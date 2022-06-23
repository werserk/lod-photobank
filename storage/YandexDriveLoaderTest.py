import yadisk

client = yadisk.YaDisk(token='<your-access-token>')
if not client.check_token():
    print("invalid yadisk token")
print("Disk info:", client.get_disk_info())


def read_files(files):
    paths = []
    for file in files:
        paths.append([])
        filepath = f"images"
        paths[-1].append(filepath)
        client.download(file, "filepath.jpg")
    print(f"Save {len(paths)} files to {filepath}")
    return paths


print(read_files(["Горы.jpg"]))
