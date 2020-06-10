include config.mk

RUN = $(LANGUAGE) $(SCRIPT)
SAM_BUILD_DIR = $(LAYLA_DIR)\.aws-sam
.DEFAULT_GOAL := build

$(LAYLA_DIR):
	mkdir -p $@
	$(RUN) \
	--directory $@ \
	--layer-name $(LAYER_NAME) \
	--contents $(CONTENTS) \
	--stack-name $(STACK_NAME) \
	--region-name $(AWS_REGION) \
	--bucket $(S3_BUCKET) \

$(SAM_BUILD_DIR): $(LAYLA_DIR)
	cd $(LAYLA_DIR) && $(SAM_CMD) build --use-container

## init: initialize .layla layer folder
.PHONY: init
init: $(LAYLA_DIR)

## build: build layer via aws-sam
.PHONY: build
build: $(SAM_BUILD_DIR)

## deploy: deploy layer via aws-sam
.PHONY: deploy
deploy: $(SAM_BUILD_DIR)
	cd $(LAYLA_DIR) && $(SAM_CMD) deploy --guided

## clean: clean everything built with LayLa
.PHONY: clean
clean:
	rm -r $(LAYLA_DIR)

.PHONY: help
help: Makefile
	@sed -n 's/^## //p' $<