PROJECTNAME=triumphum
#cp config/triumphum.troff deb/usr/share/man/man6/triumphum.1 ; gzip deb/usr/share/man/man6/triumphum.1

#cp config/_triumphum_complete deb/usr/share/zsh/vendor-completions/
DOCKERCONTAINER=${PROJECTNAME}-test-deb
DOCKERSWAPDIRECTORY=$(PWD)/docker-test

test:

builddeb:
	@echo "# Supression du repertoire"
	-rm -i --verbose --recursive deb/
	@echo "Mise en place de la hiérarchie"
	mkdir --verbose --parent deb/DEBIAN
	mkdir --verbose --parent deb/usr/bin/
	mkdir --verbose --parent deb/usr/lib/python3/dist-packages/triumphum
	mkdir --verbose --parent deb/usr/bin/
	@echo "# Copie des fichiers à leur emplacement idoine"
	cp --verbose config/control deb/DEBIAN/
	cp --verbose main.py deb/usr/bin/${PROJECTNAME}
	chmod +x deb/usr/bin/${PROJECTNAME}
	#for file in `git ls-files triumphum/` ; do cp --verbose ${file} deb/usr/lib/python3/dist-packages/ ; done
	for file in $(shell git ls-files triumphum/) ; do cp --verbose $$file deb/usr/lib/python3/dist-packages/triumphum ; done
	@echo "# Construction du paquet"
	dpkg-deb --root-owner-group --build deb ${PROJECTNAME}.deb

testdeb:
	@echo "# Nétoyage du repertoire si besoin"
	echo ${DOCKERSWAPDIRECTORY}
	-rm -i --verbose --recursive ${DOCKERSWAPDIRECTORY}/*
	@echo "# Création du repertoire si besoin"
	-mkdir ${DOCKERSWAPDIRECTORY}
	cp ${PROJECTNAME}.deb ${DOCKERSWAPDIRECTORY}
	@echo "# Extinction du conteneur si besoin"
	-docker stop ${DOCKERCONTAINER}
	@echo "# Lancement du conteneur"
	#docker run --name ${DOCKERCONTAINER} -it --rm -v ${DOCKERSWAPDIRECTORY}:/mnt debian:bookworm-slim "apt-get update ; dpkg -i /mnt/${PROJECTNAME}.deb ; triumphum ; bash"
	docker run --name ${DOCKERCONTAINER} -it --rm -v ${DOCKERSWAPDIRECTORY}:/mnt debian:bookworm-slim bash -c "apt-get update ; dpkg -i /mnt/${PROJECTNAME}.deb ; apt-get install --fix-broken --assume-yes; triumphum ; bash"

man:
	cp config/${PROJECTNAME}.troff deb/usr/share/man/man6/${PROJECTNAME}.1 ; gzip deb/usr/share/man/man6/${PROJECTNAME}.1

autocomplete:
	echo "Nothing to do"

