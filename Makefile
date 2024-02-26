IMG := ysakashita/python-merossiot
TAG := 3.9.18-0.4.6.2

.PHONY: build-image
build-image: 
	docker buildx build --platform linux/arm64 -t $(IMG):$(TAG) --load .

.PHONY: push-image
push-image: build-image
	docker push $(IMG):$(TAG)
