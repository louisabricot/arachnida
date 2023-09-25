from tools.download import generate_unique_fullpath
import os


def test_unique_name():
    iteration = 100
    download_directory = "testing"
    url_image = "https://avatars.githubusercontent.com/u/45848751?v=4"
    if not os.path.exists(download_directory):
        os.mkdir(download_directory)

    pathname = os.path.basename(url_image)
    generated_names = set()
    for _ in range(iteration):
        name = generate_unique_fullpath(pathname, download_directory)
        f = open(name, "x")
        f.close()
        generated_names.add(name)

    assert len(generated_names) == iteration
