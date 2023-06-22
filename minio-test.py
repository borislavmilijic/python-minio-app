from minio import Minio
from minio.error import S3Error


def main():
    # Create a client with the MinIO server playground, its access key
    # and secret key.
    client = Minio(
        "192.168.103.115:9000",
        access_key="eMGlzS6htbj0yoDHMByI",
        secret_key="OXkOTQEunJx8o89UztkkDXhYMORewlOjZb2fSAfo",
        secure=False

    )

    # Make 'client.2.bucket' bucket if not exist.
    found = client.bucket_exists("client.2.bucket")
    if not found:
        client.make_bucket("client.2.bucket")
    else:
        print("Bucket 'client.2.bucket' already exists")

    # Upload '/home/user/Photos/asiaphotos.zip' as object name
    # 'asiaphotos-2015.zip' to bucket 'client.2.bucket'.
    client.fput_object(
        "client.2.bucket", "asiaphotos-2015.zip", "/home/vs/projects/minio/asiaphotos-2015.zip",
    )
    print(
        "'/home/user/Photos/asiaphotos.zip' is successfully uploaded as "
        "object 'asiaphotos-2015.zip' to bucket 'client.2.bucket'."
    )


if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("error occurred.", exc)