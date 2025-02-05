PROJECTNAME=triumphum
#cp config/triumphum.troff deb/usr/share/man/man6/triumphum.1 ; gzip deb/usr/share/man/man6/triumphum.1

#cp config/_triumphum_complete deb/usr/share/zsh/vendor-completions/
DOCKERCONTAINER=${PROJECTNAME}-test-deb
DOCKERSWAPDIRECTORY=$(PWD)/docker-test
DEBDIRECTORY=$(PWD)/deb

getcurrentversion:
	@cat .bumpversion.cfg | grep "current_version =" | sed "s/.* = \(.*\)/\1/"

builddeb:
	@echo "# Supression du repertoire"
	-rm --verbose --recursive ${DEBDIRECTORY}/
	@echo "# Mise en place de la hiérarchie"
	mkdir --verbose --parent ${DEBDIRECTORY}/DEBIAN
	mkdir --verbose --parent ${DEBDIRECTORY}/usr/games/
	mkdir --verbose --parent ${DEBDIRECTORY}/usr/lib/python3/dist-packages/triumphum
	mkdir --verbose --parent ${DEBDIRECTORY}/usr/share/doc/triumphum/
	mkdir --verbose --parent ${DEBDIRECTORY}/usr/share/man/man6/
	mkdir --verbose --parent ${DEBDIRECTORY}/usr/share/zsh/vendor-completions/
	mkdir --verbose --parent ${DEBDIRECTORY}/usr/share/bash-completion/completions
	@echo "# Copie des fichiers de construction à leur emplacement idoine"
	cp --verbose config/control ${DEBDIRECTORY}/DEBIAN/
	#fold -s -w 80 config/control > ${DEBDIRECTORY}/DEBIAN/control
	cp --verbose config/copyright ${DEBDIRECTORY}/usr/share/doc/triumphum/
	cp --verbose config/LICENSE ${DEBDIRECTORY}/usr/share/doc/triumphum/
	gzip --verbose --no-name -9 --to-stdout config/changelog > ${DEBDIRECTORY}/usr/share/doc/triumphum/changelog.gz
	@echo "# Copie des éxecutables"
	cp --verbose main.py ${DEBDIRECTORY}/usr/games/${PROJECTNAME}
	chmod +x ${DEBDIRECTORY}/usr/games/${PROJECTNAME}
	for file in $(shell git ls-files triumphum/) ; do cp --verbose $$file ${DEBDIRECTORY}/usr/lib/python3/dist-packages/triumphum ; done
	@echo "# Copie de la page de manuel"
	gzip --verbose --no-name -9 --to-stdout config/triumphum.troff > ${DEBDIRECTORY}/usr/share/man/man6/triumphum.6.gz
	chmod 644 ${DEBDIRECTORY}/usr/share/man/man6/triumphum.6.gz
	@echo "# Copie de l’autocompletion pour zsh"
	cp --verbose config/zsh-completion.zsh ${DEBDIRECTORY}/usr/share/zsh/vendor-completions/_triumphum
	@echo "# Copie de l’autocompletion pour bash"
	cp --verbose config/bash-completion.bash ${DEBDIRECTORY}/usr/share/bash-completion/completions/triumphum
	@echo "# Construction du paquet"
	dpkg-deb --root-owner-group --build deb ${PROJECTNAME}.deb
	lintian triumphum.deb


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
	docker run --name ${DOCKERCONTAINER} -it --rm -v ${DOCKERSWAPDIRECTORY}:/mnt debian:bookworm-slim bash -c "apt-get update ; apt-get install --assume-yes man manpages man-db ; mandb ; PATH=$$PATH/:/usr/games ; dpkg -i /mnt/${PROJECTNAME}.deb ; apt-get install --fix-broken --assume-yes; triumphum ; bash"

man:
	cp config/${PROJECTNAME}.troff ${DEBDIRECTORY}/usr/share/man/man6/${PROJECTNAME}.1 ; gzip ${DEBDIRECTORY}/usr/share/man/man6/${PROJECTNAME}.1

autocomplete:
	echo "Nothing to do"

images:
	inkscape --export-text-to-path --export-filename=logo-blanc-version.vectorized.svg logo-blanc-version.svg
