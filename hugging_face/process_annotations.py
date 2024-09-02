import argparse
import json
import shutil
import tempfile

annotationReplacementList = [
    ('The image showcases ', ''),
    ('The image portrays ', ''),
    ('The image appears to be ', ''),
    ('The image is ', ''),
    ('The image depicts ', ''),
    ('The image features ', ''),
    ('The image captures ', ''),
    ('The image shows ', ''),
    ('The image displays ', ''),
    ('The image presents ', ''),
    ('This image showcases ', ''),
    ('This image portrays ', ''),
    ('This image appears to be ', ''),
    ('This image is ', ''),
    ('This image depicts ', ''),
    ('This image features ', ''),
    ('This image captures ', ''),
    ('This image shows ', ''),
    ('This image displays ', ''),
    ('This image presents ', ''),
    ('In this picture, ', ''),
    ('In this artwork, ', 'Artwork of '),
    ('In this illustration, ', 'Illustration of '),
    ('In this depiction, ', ''),
    ('In this piece, ', ''),
    ('In this image, ', ''),
    ('In this art piece, ', 'Art of '),
    ('In this scene, ', ''),
    ('In the picture, ', ''),
    ('In the artwork, ', 'Artwork of '),
    ('In the illustration, ', 'Illustration of '),
    ('In the depiction, ', ''),
    ('In the piece, ', ''),
    ('In the image, ', ''),
    ('In the art piece, ', 'Art of '),
    ('In the scene, ', ''),
]


def clean_annotation(annotation: str) -> str:
    cleaned_annotation = annotation
    for old, new in annotationReplacementList:
        cleaned_annotation = cleaned_annotation.replace(old, new)

    return cleaned_annotation


def clean_all_annotations(dataset_file: str) -> None:
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)

    with open(dataset_file, 'r') as input_jsonl:
        for line in input_jsonl:
            data = json.loads(line)

            for annotation in data["annotations"]:
                cleaned_annotation = clean_annotation(annotation["annotation"]["text"])
                annotation["annotation"]["clean_text"] = cleaned_annotation

            json.dump(data, temp_file)
            temp_file.write('\n')

    temp_file.close()
    shutil.move(temp_file.name, dataset_file)


def main() -> None:
    parser = argparse.ArgumentParser(description="Process JSONL dataset file and clean all annotations.")
    parser.add_argument("-f", "--dataset_file", help="Path to the input JSONL file")
    args = parser.parse_args()

    clean_all_annotations(args.dataset_file)


if __name__ == "__main__":
    main()
