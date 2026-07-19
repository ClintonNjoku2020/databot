import zipfile
from io import BytesIO

import artifact_generator


def test_generate_artifacts_creates_downloadable_files():
    csv_bytes = b"region,revenue\nNorth,120\nSouth,180\nEast,90\n"

    artifacts = artifact_generator.generate_artifacts(
        "Quarterly Revenue",
        "Create a concise executive summary.",
        "Revenue improved in the South\nEast needs follow-up",
        csv_bytes,
    )

    assert artifacts["pdf"].startswith(b"%PDF-1.4")
    assert b"<svg" in artifacts["chart_svg"]
    assert b"North" in artifacts["chart_svg"]
    assert b"<svg" in artifacts["diagram_svg"]
    assert b"Step 1" in artifacts["diagram_svg"]

    with zipfile.ZipFile(BytesIO(artifacts["pptx"])) as pptx:
        names = set(pptx.namelist())

    assert "[Content_Types].xml" in names
    assert "ppt/presentation.xml" in names
    assert "ppt/slides/slide1.xml" in names
    assert "ppt/slides/slide2.xml" in names
    assert "ppt/slides/slide3.xml" in names


def test_safe_filename_uses_plain_slug():
    assert artifact_generator.safe_filename("Q4 Revenue: North/South", "pptx") == "q4-revenue-north-south.pptx"
