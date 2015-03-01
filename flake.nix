{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-20.09";

  outputs = {
    self,
    nixpkgs,
    ...
    } @ inputs:
  let
    systems = [
      "x86_64-linux"
      "aarch64-linux"
    ];
    forAllSystems = f: nixpkgs.lib.genAttrs systems (system: f {
      inherit system;
      pkgs = nixpkgs.legacyPackages.${system};
      lib = nixpkgs.legacyPackages.${system}.lib;
    });
    mkPkgs = pkgs: with pkgs; [
      (python.withPackages (ps: with ps; [
        pygame
      ]))
      # Windows cmd.exe reimplementations
      (pkgs.writeScriptBin "cls" ''
        #!${pkgs.bash}/bin/bash
        clear
      '')
      (pkgs.writeScriptBin "color" ''
        #!${pkgs.bash}/bin/bash
        true # dgaf /shrug
      '')
    ];
  in {
    inherit inputs;

    packages = forAllSystems ({ pkgs, lib, ... }: rec {
      nerd-olympics = pkgs.writeScriptBin "nerd-olympics" ''
        #!${pkgs.bash}/bin/bash
        export PATH="${lib.makeBinPath (mkPkgs pkgs)}:$PATH"
        cd ${./.}
        python2 main.py "$@"
      '';
      default = nerd-olympics;
    });

    apps = forAllSystems ({ system, ... }: rec {
      nerd-olympics.type = "app";
      nerd-olympics.program = "${self.packages.${system}.nerd-olympics}/bin/nerd-olympics";
      default = nerd-olympics;
    });

    devShells = forAllSystems ({ pkgs, ... }: {
      default = pkgs.mkShell {
        buildInputs = mkPkgs pkgs;
      };
    });

  };
}
