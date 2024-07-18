# docker-workspaces
Docker image for workspaces admin tools

install docker add this to your bash profile

workspaces(){
        docker run --rm -it \
        -v ~/.aws:/root/.aws \
        joelhutson/workspaces:dev \
	$@
}
