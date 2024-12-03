#!/bin/bash

# Function to display usage information
usage() {
    echo "Usage: $0 <DESTINATION_SERVER> <IMAGE_NAME_WITH_TAG1> <IMAGE_NAME_WITH_TAG2> ..."
    echo "Options:"
    echo "  --help      Show this help message"
    exit 1
}

# Check for help option
if [[ "$1" == "--help" ]]; then
    usage
fi

# Check if at least one image name with tag is provided
if [ "$#" -lt 2 ]; then
    usage
fi

DESTINATION_SERVER="$1" # The first argument is the destination server
DESTINATION_REGISTRY="PRIVATE_REGISTRY"

# Loop through each image name with tag provided as arguments (starting from the second argument)
shift # Remove the first argument (destination server)
for IMAGE_NAME_WITH_TAG in "$@"; do
    DESTINATION_IMAGE_NAME="${DESTINATION_REGISTRY}/${IMAGE_NAME_WITH_TAG}"

    # Step 1: Pull the image from docker.arvancloud.ir
    echo "Pulling image ${IMAGE_NAME_WITH_TAG} from docker.arvancloud.ir..."
    docker pull docker.arvancloud.ir/${IMAGE_NAME_WITH_TAG}

    # Step 2: Tag the image for the new registry
    echo "Tagging image as ${DESTINATION_IMAGE_NAME}..."
    docker tag docker.arvancloud.ir/${IMAGE_NAME_WITH_TAG} ${DESTINATION_IMAGE_NAME}

    # Step 3: Push the image to the new registry
    echo "Pushing image to ${DESTINATION_IMAGE_NAME}..."
    docker push ${DESTINATION_IMAGE_NAME}

    # Step 4: SSH to the destination server and pull the image
    echo "SSHing to ${DESTINATION_SERVER} to pull ${DESTINATION_IMAGE_NAME}..."
    ssh root@${DESTINATION_SERVER} << EOF
        echo "Pulling image ${DESTINATION_IMAGE_NAME}..."
        docker pull ${DESTINATION_IMAGE_NAME}

        # Step 5: Tag the image as <IMAGE_NAME_WITH_TAG>
        echo "Tagging image as ${IMAGE_NAME_WITH_TAG}..."
        docker tag ${DESTINATION_IMAGE_NAME} ${IMAGE_NAME_WITH_TAG}
EOF
done

echo "Script completed successfully."
