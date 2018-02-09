import sys, json, argparse

import docker

arg_parser = argparse.ArgumentParser("docker-image-mgr")
arg_parser.add_argument("image", help='docker image name')
arg_parser.add_argument("-dh", "--dhost", help="docker daemon host ip", default=None)
arg_parser.add_argument("-dp", "--dport", help="docker daemon host port", type=int, default=2357)
arg_parser.add_argument("-c", "--cmd", help="supported docker image commands, such as list, remove, pull, remove and pull", choices=['ls', 'rmi', 'pull', 'rmi-pull'])

LOCAL_DOCKER_SOCKET = 'unix://var/run/docker.sock'

def get_base_url(dockerHost, dockerPort):
    if dockerHost is None:
        return "unix://var/run/docker.sock"
    else:
        return "tcp://" + dockerHost + ":" + str(dockerPort)

def ls_docker_image(dockerClient, dockerImage):
    image_list = dockerClient.images.list()
    found_images = []
    for image in image_list:
        image_tags = image.tags
        if len(image_tags) > 0:
            for image_tag in image_tags:
                if image_tag.startswith(dockerImage):
                    container_list = dockerClient.containers.list(filters={'ancestor': image.id})
                    running_status = True if len(container_list) > 0 else False

                    # print("Image Id: {}, full name: {}, Containers: {}".format(image.short_id, image_tag, container_list))
                    if running_status:
                        found_images.append({"image_name": image_tag, "image_id": image.id, "running": True,
                                             "containers": str(container_list)})
                    else:
                        found_images.append({"image_name": image_tag, "image_id": image.id, "running": False})

    return found_images


if __name__ == "__main__":
    args = arg_parser.parse_args()
    dockerHost = args.dhost
    dockerPort = args.dport
    dockerImage = args.image
    dockerCmd = args.cmd

    dockerClient = docker.DockerClient(base_url=get_base_url(dockerHost, dockerPort), version='auto')

    if dockerCmd == "ls":
        found_images = ls_docker_image(dockerClient, dockerImage)

        if len(found_images) > 0:
            print("Docker Images Found: ")
            print(json.dumps(found_images))
        else:
            print("No Docker Image found with {}".format(dockerImage))

    elif dockerCmd == "rmi":
        pending_remove = ls_docker_image(dockerClient, dockerImage)

        if len(pending_remove) > 0:
            print("The following Docker Image(s) will be removed ...")
            print(json.dumps(pending_remove))

            for to_remove in pending_remove:
                dockerClient.images.remove(image=to_remove["image_name"], force=True)

            print("Done")
        else:
            print("No Docker Image found with {}".format(dockerImage))

    elif dockerCmd == "pull":
        dockerClient.images.pull(dockerImage, insecure_registry=True, auth_config={})
        print("Pulled {} to local host".format(dockerImage))
        found_images = ls_docker_image(dockerClient, dockerImage)
        print(json.dumps(found_images))

    elif dockerCmd == "rmi-pull":
        pending_remove = ls_docker_image(dockerClient, dockerImage)

        if len(pending_remove) > 0:
            print("The Docker Image(s) on local host will be removed first ...")
            print(json.dumps(pending_remove))

            for to_remove in pending_remove:
                dockerClient.images.remove(image=to_remove["image_name"], force=True)

            print("Done")
        else:
            print("Docker Image {} has already been removed".format(dockerImage))

        dockerClient.images.pull(dockerImage, insecure_registry=True, auth_config={})
        print("Pulled {} to local host again ...".format(dockerImage))
        found_images = ls_docker_image(dockerClient, dockerImage)
        print(json.dumps(found_images))

    else:
        print("Invalid Cmd {} !".format(dockerCmd))
        sys.exit(-1)

    sys.exit(0)
