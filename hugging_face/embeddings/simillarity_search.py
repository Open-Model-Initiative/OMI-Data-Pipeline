from fastembed import ImageEmbedding
import chromadb
from PIL import Image
import os
from tqdm import tqdm
import argparse
import shutil


# list of supported image models
# https://qdrant.github.io/fastembed/examples/Supported_Models/
# model	                      dim	description	                                        size_in_GB
# Qdrant/resnet50-onnx	      2048	ResNet-50 from `Deep Residual Learning for Ima...	0.10
# Qdrant/clip-ViT-B-32-vision 512	CLIP vision encoder based on ViT-B/32	            0.34
# Qdrant/Unicom-ViT-B-32	  512	Unicom Unicom-ViT-B-32 from open-metric-learning	0.48
# Qdrant/Unicom-ViT-B-16	  768	Unicom Unicom-ViT-B-16 from open-metric-learning	0.82

allowed_image_extensions = Image.registered_extensions().keys()


def search_similar_images(
    folder_path: str,
    model_name: str = "Qdrant/resnet50-onnx",
    cache_path: str = "cache",
    recursive: bool = False,
    same_images_distance: float = 0.2,
    similar_images_distance: float = 0.5,
    max_similar_images: int = 10,
    show_progress: bool = True,
    batch_size: int = 32
) -> dict:
    """
        Search for similar images in a given folder using image embeddings.
        Args:
            folder_path (str): The path to the folder containing the images.
            model_name (str, optional): The name of the image embedding model to use. Defaults to "Qdrant/resnet50-onnx".
            cache_path (str, optional): The path to the cache directory. Defaults to "cache".
            recursive (bool, optional): Flag indicating whether to search for images recursively in subdirectories. Defaults to False.
            same_images_distance (float, optional): The maximum distance threshold for considering two images as the same. Defaults to 0.2.
            similar_images_distance (float, optional): The maximum distance threshold for considering two images as similar. Defaults to 0.5.
            max_similar_images (int, optional): The maximum number of similar images to retrieve for each image. Defaults to 10.
            show_progress (bool, optional): Flag indicating whether to show the progress bar. Defaults to True.
            batch_size (int, optional): The batch size for processing images. Defaults to 32.
        Returns:
            dict: A dictionary containing the paths of similar images and unique images found.
        Raises:
            FileNotFoundError: If the specified folder_path does not exist.
    """
    # get all images paths
    images_paths = []
    if recursive:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith(tuple(allowed_image_extensions)):
                    images_paths.append(os.path.join(root, file))
    else:
        for file in os.listdir(folder_path):
            if file.endswith(tuple(allowed_image_extensions)):
                images_paths.append(os.path.join(folder_path, file))

    # conveert to batches
    batches = [images_paths[i:i + batch_size] for i in range(0, len(images_paths), batch_size)]

    model = ImageEmbedding(
        model_name=model_name,
        cache_dir=cache_path
    )

    unique_images_paths = []
    similar_images_paths = []

    db = chromadb.Client()
    collection = db.create_collection("images")

    for batch in tqdm(batches, desc="Embedding images", disable=not show_progress):
        embeddings = model.embed(batch, batch_size=batch_size)
        embeddings_with_paths = list(zip(embeddings, batch))

        for embedding, path in embeddings_with_paths:
            results = collection.query(
                query_embeddings=[embedding.tolist()],
                n_results=max_similar_images,
            )

            similiar_images_count = 0
            is_dropping_image = False
            for distance in results['distances']:

                if len(distance) == 0:
                    break

                distance = distance[0]

                if distance < same_images_distance:
                    is_dropping_image = True
                    break
                elif distance < similar_images_distance:
                    similiar_images_count += 1
                    if similiar_images_count >= max_similar_images:
                        is_dropping_image = True
                        break

            if is_dropping_image:
                similar_images_paths.append(path)
            else:
                unique_images_paths.append(path)
                collection.add(
                    ids=[path],
                    embeddings=[embedding.tolist()],
                )

    return {
        'similar_images_paths': similar_images_paths,
        'unique_images_paths': unique_images_paths
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search for similar images in a given folder using image embeddings.")
    parser.add_argument("folder_path", type=str, help="The path to the folder containing the images.")
    parser.add_argument("--target_folder_path", type=str, help="The path to the target folder containing the images. If not provided, images won't be moved to the target folder.")
    parser.add_argument("--mode", type=str, default="move", help="The mode of operation. Defaults to 'move'. Options are 'move' and 'copy'.")
    parser.add_argument("--model_name", type=str, default="Qdrant/resnet50-onnx", help="The name of the image embedding model to use. Defaults to 'Qdrant/resnet50-onnx'.")
    parser.add_argument("--cache_path", type=str, default="cache", help="The path to the cache directory. Defaults to 'cache'.")
    parser.add_argument("--recursive", action="store_true", help="Flag indicating whether to search for images recursively in subdirectories.")
    parser.add_argument("--same_images_distance", type=float, default=0.2, help="The maximum distance threshold for considering two images as the same. Defaults to 0.2.")
    parser.add_argument("--similar_images_distance", type=float, default=0.5, help="The maximum distance threshold for considering two images as similar. Defaults to 0.5.")
    parser.add_argument("--max_similar_images", type=int, default=10, help="The maximum number of similar images to retrieve for each image. Defaults to 10.")
    parser.add_argument("--show_progress", action="store_true", help="Flag indicating whether to show the progress bar.")
    parser.add_argument("--batch_size", type=int, default=32, help="The batch size for processing images. Defaults to 32.")

    args = parser.parse_args()

    result = search_similar_images(
        folder_path=args.folder_path,
        model_name=args.model_name,
        cache_path=args.cache_path,
        recursive=args.recursive,
        same_images_distance=args.same_images_distance,
        similar_images_distance=args.similar_images_distance,
        max_similar_images=args.max_similar_images,
        show_progress=args.show_progress,
        batch_size=args.batch_size
    )

    mode = args.mode
    target_folder_path = args.target_folder_path

    if target_folder_path:
        similar_images_target_folder_path = os.path.join(target_folder_path, "similar_images")
        unique_images_target_folder_path = os.path.join(target_folder_path, "unique_images")

        os.makedirs(similar_images_target_folder_path, exist_ok=True)
        os.makedirs(unique_images_target_folder_path, exist_ok=True)

        if mode == "move":
            for path in result['similar_images_paths']:
                shutil.move(path, similar_images_target_folder_path)
            for path in result['unique_images_paths']:
                shutil.move(path, unique_images_target_folder_path)
        elif mode == "copy":
            for path in result['similar_images_paths']:
                shutil.copy(path, similar_images_target_folder_path)
            for path in result['unique_images_paths']:
                shutil.copy(path, unique_images_target_folder_path)
