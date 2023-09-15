FROM public.registry.bitswan.space/bitswan/bspump:2023-54-git-4c50711

LABEL src=https://github.com/bitswan-space/container-configuration-service

WORKDIR /opt/container-configuration-service

COPY ./container_config_service.py ./container_config_service.py
COPY ./ccs ./ccs

CMD ["python3", "/opt/container-configuration-service/container_config_service.py", "-c", "/conf/container_config_service.conf"]
