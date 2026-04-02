import os
import re
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from document_loader import (
    load_document,
    extract_pdf_text,
    is_scanned_pdf,
    extract_text_from_scanned_pdf,
    ocr_image_with_mistral
)

# FIX: Removed file-system cache (screening_cache.json) — Streamlit Cloud
# ephemeral filesystem resets on every deploy/restart so the cache was useless
# and could cause stale/corrupt results. In-memory cache per session instead.
_memory_cache: dict = {}

DEFAULT_MODEL = "llama-3.1-8b-instant"


def get_llm(model: str = DEFAULT_MODEL):
    from langchain_groq import ChatGroq
    return ChatGroq(
        model=model,
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0
    )


def extract_text(file_path: str) -> str:
    ext = file_path.lower().split(".")[-1]
    if ext == "pdf":
        if is_scanned_pdf(file_path):
            print(f"  [Scanned PDF] Using OCR...")
            return extract_text_from_scanned_pdf(file_path)
        else:
            docs = extract_pdf_text(file_path)
            return "\n".join(doc.page_content for doc in docs)
    elif ext == "docx":
        docs = load_document(file_path)
        return "\n".join(doc.page_content for doc in docs)
    elif ext in ["jpg", "jpeg", "png"]:
        print(f"  [Image] Using OCR...")
        return ocr_image_with_mistral(file_path)
    else:
        raise ValueError(f"Unsupported file type: .{ext}")


def normalize_text(text: str) -> str:
    return (text
        .replace("\u2013", "-")
        .replace("\u2014", "-")
        .replace("\u2212", "-")
        .replace("\u00a0", " ")
    )


def extract_json_safe(text: str) -> dict:
    text = text.strip().replace("```json", "").replace("```", "")
    try:
        return json.loads(text)
    except Exception:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except Exception:
                pass
    return {}


screen_prompt = ChatPromptTemplate.from_template("""
You are a strict and experienced HR recruiter.
Carefully read the resume and job description.
Return ONLY a valid JSON object. No markdown. No explanation.

EXTRACTION RULES:
- Extract information ONLY from what is written in the resume
- Do NOT assume or fabricate any information
- Treat abbreviations as equivalent:
  ML=Machine Learning, NLP=Natural Language Processing,
  JS=JavaScript, k8s=Kubernetes, DL=Deep Learning,
  CV=Computer Vision, AI=Artificial Intelligence etc.
- matched_skills: skills in BOTH resume AND JD
- missing_skills: required JD skills absent from resume
- experience: calculate from work dates if available

{{
    "name"          : "candidate full name exactly as written or null",
    "email"         : "email address exactly as written or null",
    "phone"         : "phone number exactly as written or null",
    "linkedin"      : "full linkedin url or null",
    "github"        : "full github url or null",
    "experience"    : "total work experience e.g. 1 month, 2 years 3 months or Not specified",
    "education"     : "highest degree exactly as written or Not specified",
    "matched_skills": ["skills found in BOTH resume and JD"],
    "missing_skills": ["required JD skills clearly absent from resume"],
    "strengths"     : "2 honest sentences about candidate strengths relative to this JD",
    "weaknesses"    : "1 honest sentence about most critical gap for this role",
    "score"         : <realistic 0-100 integer>,
    "verdict"       : "exactly one of: Strongly Recommended, Recommended, Maybe, Not Recommended"
}}

SCORING GUIDE:
80-100 → meets most or all requirements
60-79  → meets core requirements with some gaps
40-59  → meets some requirements, clear gaps
20-39  → meets few requirements
0-19   → poor match

SCORING RULES:
- Fresh graduate/intern for senior role    → max 55
- Only internship for full-time role       → deduct 15 points
- Missing more than 3 required skills      → max 60
- Exceeds experience requirement           → +5
- Has all required skills                  → min 65

VERDICT RULES:
Strongly Recommended → score >= 80 AND has most required skills
Recommended          → score >= 65 AND meets core requirements
Maybe                → score >= 40 AND has some relevant skills
Not Recommended      → score < 40 OR missing more than half required skills

Job Description:
{jd_text}

Resume:
{resume_text}
""")


def screen_resume(resume_path: str, jd_text: str, model: str = DEFAULT_MODEL) -> dict:
    # FIX: in-memory cache keyed by path + model (valid within one Streamlit session)
    cache_key = f"{resume_path}_{model}"
    if cache_key in _memory_cache:
        print(f"  [cached ⚡] {os.path.basename(resume_path)}")
        return _memory_cache[cache_key]

    try:
        resume_text = normalize_text(extract_text(resume_path))
    except Exception as e:
        print(f"  ❌ Extraction failed: {resume_path} → {e}")
        return None

    if not resume_text.strip():
        print(f"  ❌ Empty text: {resume_path}")
        return None

    llm   = get_llm(model)
    chain = screen_prompt | llm | StrOutputParser()

    try:
        raw    = chain.invoke({"jd_text": jd_text, "resume_text": resume_text})
        parsed = extract_json_safe(raw)
        if not parsed:
            print(f"  ⚠️  Empty response: {os.path.basename(resume_path)}")
            return None
    except Exception as e:
        print(f"  ❌ LLM failed: {resume_path} → {e}")
        return None

    verdict_map = {
        "strongly recommended": "✅ Strongly Recommended",
        "recommended"         : "⚠️  Recommended",
        "maybe"               : "🔶 Maybe",
        "not recommended"     : "❌ Not Recommended"
    }
    raw_verdict = str(parsed.get("verdict", "")).lower()
    verdict     = next((v for k, v in verdict_map.items() if k in raw_verdict), "🔶 Maybe")

    result = {
        "filename"      : os.path.basename(resume_path),
        "name"          : parsed.get("name"),
        "email"         : parsed.get("email"),
        "phone"         : parsed.get("phone"),
        "linkedin"      : parsed.get("linkedin"),
        "github"        : parsed.get("github"),
        "experience"    : parsed.get("experience",    "Not specified"),
        "education"     : parsed.get("education",     "Not specified"),
        "matched_skills": parsed.get("matched_skills", []),
        "missing_skills": parsed.get("missing_skills", []),
        "strengths"     : parsed.get("strengths",     ""),
        "weaknesses"    : parsed.get("weaknesses",    ""),
        "score"         : int(parsed.get("score") or 0),
        "verdict"       : verdict,
        "model"         : model
    }

    _memory_cache[cache_key] = result
    return result


def screen_all(resume_paths: list, jd_path: str, model: str = DEFAULT_MODEL) -> list:
    print(f"\n📋 Loading Job Description...")
    print(f"   Model: {model}")

    try:
        jd_text = normalize_text(extract_text(jd_path))
    except Exception as e:
        print(f"❌ Failed to load JD: {e}")
        return []

    print(f"✅ JD loaded ({len(jd_text)} chars)")
    print(f"\n👥 Screening {len(resume_paths)} resume(s) in parallel...\n")

    results = []
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            executor.submit(screen_resume, path, jd_text, model): path
            for path in resume_paths
        }
        for future in as_completed(futures):
            path = futures[future]
            try:
                result = future.result()
                if result:
                    results.append(result)
                    print(f"  ✅ Done: {os.path.basename(path)} → {result['score']}%")
            except Exception as e:
                print(f"  ❌ Failed: {path} → {e}")

    results.sort(key=lambda x: x["score"], reverse=True)
    return results