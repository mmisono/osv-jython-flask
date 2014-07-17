.PHONY: module clean

module: upstream apps

upstream:
	./GET

apps:
	./INSTALL_APP

clean:
	rm -rf tmp/ ROOTFS/

