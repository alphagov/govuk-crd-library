let
  pkgs = import <nixpkgs> { };
in pkgs.mkShellNoCC {
  packages = with pkgs; [
    python3
    git
    kubernetes-helm
  ];

  shellHook = ''
  python -m venv env
  source ./env/bin/activate
  pip install -r src/requirements.txt
  '';
}
