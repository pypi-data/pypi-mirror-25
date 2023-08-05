def get_file_type(fp):
    magic_numbers = [
        (b"\x4D\x5A", "PE"),
        (b"\xCE\xFA\xED\xFE", "MachO"),
        (b"\xCF\xFA\xED\xFE", "MachO"),
        (b"\xBE\xBA\xFE\xCA", "MachO"),
        (b"\xBF\xBA\xFE\xCA", "MachO"),
        (b"\x7F\x45\x4C\x46\x01", "ELF-Linux"),
        (b"\x7F\x45\x4C\x46\x02", "ELF-Linux")
    ]

    max_read_len = max([len(m[0]) for m in magic_numbers])
    fileheader = fp.read(max_read_len)
    for magic, filetype in magic_numbers:
        if fileheader[:len(magic)] == magic:
            return filetype

    return None

