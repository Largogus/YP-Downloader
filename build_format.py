def build_format(h: int) -> str:
    return (
        f"bv*[height<={h}][vcodec^=avc1]+ba[ext=m4a]"
        f"/bv*[height<={h}]+ba[ext=m4a]"
        f"/bv*[height<={h}]+ba"
        f"/b[height<={h}]/b"
    )