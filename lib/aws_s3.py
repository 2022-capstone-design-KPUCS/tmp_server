import boto3

def s3_connection():
    try:
        s3 = boto3.client(
            service_name="s3",
            # region_name="ap-northeast-2", # 자신이 설정한 bucket region
            # aws_access_key_id=config("aws_access_key_id"),
            # aws_secret_access_key=config("aws_secret_access_key"),
        )
    except Exception as e:
        print(e)
    else:
        print("s3 bucket connected!")
        return s3

def s3_put_object(s3, bucket, filepath):
    """
    s3 bucket에 지정 파일 업로드
    :param s3: 연결된 s3 객체(boto3 client)
    :param bucket: 버킷명
    :param filepath: 파일 위치
    :param access_key: 저장 파일명
    :return: 성공 시 True, 실패 시 False 반환
    """
    try:
        s3.upload_file(
            filepath,
            bucket,
            filepath,
        )
    except Exception as e:
        return False
    return True

def s3_get_image_url(s3, filename):
    """
    s3 : 연결된 s3 객체(boto3 client)
    filename : s3에 저장된 파일 명
    """
    location = s3.get_bucket_location(Bucket="sangwoha-bucket")["LocationConstraint"]
    return f"https://sangwoha-bucket.s3.{location}.amazonaws.com/{filename}.png"

def s3_get_image(s3, bucket, filename):
    from PIL import Image
    response = s3.get_object(Bucket=bucket, Key="test.jpg")
    print(response)

if __name__ == '__main__':
  bucket_name = "sangwoha-bucket"
#   file_name = "0.jpg"
#   # test img file

  s3 = s3_connection()
  s3_get_image(s3, bucket_name, "test.jpg")
#   s3_put_object(s3, bucket_name, file_name)
#   # os.system("curl " + s3_get_image_url(s3, "static") + " > test.png")
