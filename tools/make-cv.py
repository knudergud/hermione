#!/usr/bin/env python3
"""Generate assets/hermione-granger-cv.pdf.

Pure standard library: writes a minimal one-page PDF using the base-14 fonts,
so the repository stays dependency-free. Run from the repository root:

    python3 tools/make-cv.py
"""
import pathlib
import zlib

WIDTH, HEIGHT = 595.28, 841.89  # A4 in points
LEFT = 56
OUT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "hermione-granger-cv.pdf"

# (style, text) where style picks font/size/leading.
LINES = [
    ("h1", "Hermione Jean Granger"),
    ("meta", "Head, Department of Magical Law Enforcement  ·  London, United Kingdom"),
    ("meta", "hello@hermionegranger.example  ·  hermionegranger.example"),
    ("gap", ""),
    ("h2", "Profile"),
    ("body", "Magical-law practitioner working at the point where research becomes statute."),
    ("body", "Twenty-two years of institutional reform, creature-rights advocacy, and"),
    ("body", "evidence review across the Ministry of Magic and the Wizengamot."),
    ("gap", ""),
    ("h2", "Experience"),
    ("h3", "Head, Department of Magical Law Enforcement   2019-present"),
    ("body", "Lead 340 staff across Auror, Wizengamot Administration, and Improper Use of"),
    ("body", "Magic services. Introduced recorded testimony, ended Veritaserum in sentencing,"),
    ("body", "and published the first open register of Azkaban detentions."),
    ("h3", "Deputy Head, Regulation and Control of Magical Creatures   2013-2019"),
    ("body", "Authored the Elf Labour Act (2016): wage floors, refusal rights, and an"),
    ("body", "independent complaints body. Negotiated the centaur border accords."),
    ("h3", "Senior Counsel, Wizengamot Reform Commission   2004-2013"),
    ("body", "Reviewed 1,100 wartime convictions; 94 were overturned. The review method is"),
    ("body", "now standard practice across three ministries."),
    ("h3", "Founder, S.P.E.W.   1998-2004"),
    ("body", "Built the advocacy body that supplied the evidence base for the Elf Labour Act."),
    ("gap", ""),
    ("h2", "Selected writing"),
    ("body", "Who Counts as a Being? Journal of Magical Jurisprudence, 2024."),
    ("body", "Evidence After the War. Wizengamot Review, 2022."),
    ("body", "Against Benevolence. The Quibbler, 2020."),
    ("gap", ""),
    ("h2", "Education and honours"),
    ("body", "Hogwarts School of Witchcraft and Wizardry, N.E.W.T.s 1998."),
    ("body", "Order of Merlin, First Class, 1999."),
]

STYLES = {
    "h1": ("F2", 22, 30),
    "h2": ("F2", 13, 22),
    "h3": ("F3", 11, 17),
    "meta": ("F1", 10, 14),
    "body": ("F1", 10.5, 15),
    "gap": ("F1", 10, 10),
}


def escape(text):
    return text.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")


def content_stream():
    parts = ["BT", f"1 0 0 1 {LEFT} {HEIGHT - 72} Tm"]
    for style, text in LINES:
        font, size, leading = STYLES[style]
        parts.append(f"/{font} {size} Tf {leading} TL")
        parts.append(f"({escape(text)}) Tj T*" if text else "T*")
    parts.append("ET")
    return "\n".join(parts).encode("latin-1")


def build():
    stream = zlib.compress(content_stream())
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        (
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {WIDTH:.2f} {HEIGHT:.2f}] "
            "/Resources << /Font << /F1 5 0 R /F2 6 0 R /F3 7 0 R >> >> /Contents 4 0 R >>"
        ).encode("latin-1"),
        b"<< /Length " + str(len(stream)).encode() + b" /Filter /FlateDecode >>\nstream\n" + stream + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Times-Bold /Encoding /WinAnsiEncoding >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>",
    ]

    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = []
    for number, body in enumerate(objects, start=1):
        offsets.append(len(out))
        out += f"{number} 0 obj\n".encode() + body + b"\nendobj\n"

    xref_at = len(out)
    out += f"xref\n0 {len(objects) + 1}\n".encode()
    out += b"0000000000 65535 f \n"
    for offset in offsets:
        out += f"{offset:010d} 00000 n \n".encode()
    out += (
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_at}\n%%EOF\n"
    ).encode()

    OUT.write_bytes(bytes(out))
    print(f"wrote {OUT} ({len(out)} bytes)")


if __name__ == "__main__":
    build()
