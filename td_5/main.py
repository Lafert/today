import requests
import img2pdf
from PIL import Image



def convert_to_jp2(image_path, output_path):
    img = Image.open(image_path)
    img.save(output_path, "JPEG2000")
def get_data():

    headers = {
        'Uaer_Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }

    img_list = []
    for i in range(1,11):
        url = f'https://image.isu.pub/210803133455-9d8c07773d1ae8549a34ed3127d6f9d6/jpg/page_{i}_thumb_large.jpg'
        response = requests.get(url, headers=headers).content
        with open(f'media/{i}.jpg', 'wb') as file:
            file.write(response)
            img_list.append(f'media/{i}.jpg')
            print(f'Download {i} of 139')
            # try:
            #     img = Image.open(f'media/{i}.jpg')
            # except (IOError, OSError):
            #     print(f'Error opening image: {i}.jpg')
            # else:
            #     img.close()

    print('#'*20)
    print(img_list)

    jp2_list = []
    for img_path in img_list:
        jp2_path = img_path.replace(".jpg", ".jp2")
        convert_to_jp2(img_path, jp2_path)
        jp2_list.append(jp2_path)

    with open('book.pdf', 'wb') as file:
        file.write(img2pdf.convert(jp2_list))

    print('PDF file created successfully')

def main():
    get_data()

if __name__ == "__main__":
    main()

# разобраться как создавать книгу с уже скачаных файлов, чтоб не перекачивать заново, прочитать через os
