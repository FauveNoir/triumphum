PROJECTNAME=triumphum
#cp config/triumphum.troff deb/usr/share/man/man6/triumphum.1 ; gzip deb/usr/share/man/man6/triumphum.1

#cp config/_triumphum_complete deb/usr/share/zsh/vendor-completions/
DOCKERCONTAINER=${PROJECTNAME}-test-deb
DOCKERSWAPDIRECTORY=$(PWD)/docker-test
DEBDIRECTORY=$(PWD)/deb


builddeb:
	@echo "# Supression du repertoire"
	-rm --verbose --recursive ${DEBDIRECTORY}/
	@echo "# Mise en place de la hiérarchie"
	mkdir --verbose --parent ${DEBDIRECTORY}/DEBIAN
	mkdir --verbose --parent ${DEBDIRECTORY}/usr/games/
	mkdir --verbose --parent ${DEBDIRECTORY}/usr/lib/python3/dist-packages/triumphum
	@echo "# Copie des fichiers à leur emplacement idoine"
	cp --verbose config/control ${DEBDIRECTORY}/DEBIAN/
	cp --verbose main.py ${DEBDIRECTORY}/usr/games/${PROJECTNAME}
	chmod +x ${DEBDIRECTORY}/usr/games/${PROJECTNAME}
	for file in $(shell git ls-files triumphum/) ; do cp --verbose $$file ${DEBDIRECTORY}/usr/lib/python3/dist-packages/triumphum ; done
	@echo "# Copie de la page de manuel"
	mkdir --verbose --parent ${DEBDIRECTORY}/usr/share/man/man6/
	gzip --to-stdout config/triumphum.troff > ${DEBDIRECTORY}/usr/share/man/man6/triumphum.6.gz
	chmod 644 ${DEBDIRECTORY}/usr/share/man/man6/triumphum.6.gz
	@echo "# Copie de l’autocompletion pour zsh"
	mkdir --verbose --parent ${DEBDIRECTORY}/usr/share/zsh/vendor-completions/
	cp --verbose config/zsh-completion.zsh ${DEBDIRECTORY}/usr/share/zsh/vendor-completions/_triumphum
	@echo "# Copie de l’autocompletion pour bash"
	mkdir --verbose --parent ${DEBDIRECTORY}/usr/share/bash-completion/completions
	cp --verbose config/bash-completion.bash ${DEBDIRECTORY}/usr/share/bash-completion/completions/triumphum
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
	docker run --name ${DOCKERCONTAINER} -it --rm -v ${DOCKERSWAPDIRECTORY}:/mnt debian:bookworm-slim bash -c "apt-get update ; apt-get install --assume-yes man manpages man-db ; mandb ; PATH=$$PATH/:/usr/games ; dpkg -i /mnt/${PROJECTNAME}.deb ; apt-get install --fix-broken --assume-yes; triumphum ; bash"

man:
	cp config/${PROJECTNAME}.troff ${DEBDIRECTORY}/usr/share/man/man6/${PROJECTNAME}.1 ; gzip ${DEBDIRECTORY}/usr/share/man/man6/${PROJECTNAME}.1

autocomplete:
	echo "Nothing to do"

