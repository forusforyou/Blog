import hashlib
from blog.settings import MD5SALT

def md5_encryption(pwd):
    content = pwd + MD5SALT
    md = hashlib.md5()
    md.update(content.encode())
    return md.hexdigest()


if __name__ == "__main__":
    print(md5_encryption("123"))