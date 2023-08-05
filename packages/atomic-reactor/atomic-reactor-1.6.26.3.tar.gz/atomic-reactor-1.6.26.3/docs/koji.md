## Koji integration

The `add_filesystem`, `koji`, `fetch_maven_artifacts`, `inject_parent_image` pre-build plugins and the `koji_promote` and `koji_tag_build` exit plugins provide integration with [Koji](https://docs.pagure.org/koji/).

## Pre-build plugins

The `add_filesystem` pre-build plugin provides special handling for images with "FROM koji/image-build". For these images it creates a Koji task to create a installed filesystem archive as [described here](https://github.com/projectatomic/atomic-reactor/blob/master/docs/base_images.md).

The `koji` pre-build plugin creates a yum repofile to allow instructions in the Dockerfile to have access to RPMs available from the appropriate Koji tag.

The `koji_parent` pre-build plugin determines the expected NVR (Name-Version-Release) of the Koji build for the parent image. It waits for a given amount if build does not exist yet.

The `fetch_maven_artifacts` pre-build plugin will use configuration files to download external maven artifacts. One of these sources can be a Koji build.

The `inject_parent_image` pre-build plugin overwrites the parent image to be used based on a given Koji build.

## Exit plugins

The `koji_promote` exit plugin uses the [Koji Content Generator API](https://docs.pagure.org/koji/content_generators/) to import the built image, and logs generated during the build, into Koji.

When importing a build using the Content Generator API, metadata to describe the build is generated. This follows [the metadata format specification](https://docs.pagure.org/koji/content_generator_metadata/) but in some cases content generators are free to choose how metadata is expressed.

Each build creates a single output archive, in the [Combined Image JSON + Filesystem Changeset format](https://github.com/docker/docker/blob/master/image/spec/v1.2.md#combined-image-json--filesystem-changeset-format).

This plugin will also tag the imported build, if `koji_tag_build` is *not* configured. Otherwise, it assumes `koji_tag_build` will perform build tagging.

The `koji_upload` and `koji_import` plugins work in conjuction as a replacement to `koji_promote`.
`koji_upload` runs as a post build plugin in the worker build to upload platform specific to koji,
and capture platform specifc metadata.
`koji_import` runs as an exit plugin in the orchestrator build to gather the platform specific
metadata from each worker build and combine into a single build to be imported into Koji via
[Koji Content Generator API](https://docs.pagure.org/koji/content_generators/).

The `koji_tag_build` exit plugin is used to tag the imported koji build based on a target. [Koji Tags and Targets](https://docs.pagure.org/koji/#tags-and-targets)

# Type-specific build metadata

For atomic-reactor container image builds the `image` type is used, and so type-specific information is placed into the `build.extra.image` map. Note that this does not use `build.extra.typeinfo.image` -- the `typeinfo` element was introduced after the `image` type started to be used.

Data which is placed here includes:

- `build.extra.image.autorebuild` (boolean): true if this build was triggered automatically; false otherwise
- `build.extra.image.help` (string or null): filename of the markdown help file in the repository if this build has a markdown help converted to man page; null otherwise
- `build.extra.container_koji_task_id` (int): Koji task ID which created the BuildConfig for this OpenShift Build -- note that this location is technically incorrect but remains as-is for compatibility with existing software
- `build.extra.filesystem_koji_task_id` (int): Koji task ID which atomic-reactor created in order to generate the initial layer of the image (for "FROM koji/image-build" images) -- note that this location is technically incorrect but remains as-is for compatibility with existing software
- `build.extra.media_types` (str list): Container image media types for which this image is available, where "application/json" is for a Docker Registry HTTP API V1 image; currently this key is only set when Pulp integration is enabled

# Type-specific buildroot metadata:

In each buildroot, the extra.osbs key is used to define a map that contains these items:

- `build_id` (string): the build ID which resulted in the buildroot currently running atomic-reactor (**currently incorrect**)
- `builder_image_id` (string): the docker pull-by-digest specification for the buildroot currently running atomic-reactor

# Type-specific output metadata:

Each output has a type field. The docker image archive output is identified by type "docker-image", and has these type-specific data:

- `extra.image.arch` (string): architecture for this image archive
- `extra.docker` (map): information specific to the Docker image

The docker map has these entries:

- `id` (string): the image ID -- for Docker 1.10 and higher this is a content-aware image ID
- `parent_id` (string): the image ID of the parent image
- `repositories` (string list): docker pull specifications for the name:version-release image in the docker registry (or in Crane, if Pulp/Crane integration is used)
- `config` (map): the [v2 schema 2 'config' object](https://docs.docker.com/registry/spec/manifest-v2-2/#image-manifest-field-descriptions) but with the 'container_config' entry removed
- `tags` (string list): the image tags (i.e. the part after the ":") applied to this image when it was tagged and pushed

## Example

Example type-specific content generator metadata in context:

```json
{
  "metadata_version": 0,
  "build": {
    "name": "package-name-docker",
    "version": "1.0.0",
    "release": "1",
    "extra": {
      "image": {
        "autorebuild": false,
        "help": null
      },
      "filesystem_koji_task_id": 123457,
      "container_koji_task_id": 123456
    },
    "start_time": ...,
    "end_time": ...,
    "source": "git://...#..."
  },
  "buildroots": [
    {
      "id": 1,
      "container": {
        "type": "docker",
        "arch": "x86_64"
      },
      "extra": {
        "osbs": {
          "build_id": "(should be build which created the buildroot image)",
          "builder_image_id": "docker-pullable://.../buildroot@sha256:abcdef..."
        }
      },
      "content_generator": {
        "name": "atomic-reactor",
        "version": "1.2.3"
      },
      "host": {...},
      "components": [...],
      "tools": [...]
    }
  ],
  "output": [
    {
      "type": "docker-image",
      "extra": {
        "image": {
          "arch": "x86_64"
        }
      },
      "docker": {
        "id": "sha256:abc123def...",
        "parent_id": "sha256:123def456...",
        "repositories": [
          "registry.example.com/product/package-name:1.0.0-1",
          "registry.example.com/product/package-name@sha256:123def..."
        ],
        "config": {
          "docker_version": "1.10.3",
          "rootfs": {...},
          "config": {...},
          ...
        },
        "tags": [
          "latest",
          "1.0.0-1",
          "1.0.0"
        ]
      },
      "components": [...],
      ...
    },
    ...
  ]
}
```
