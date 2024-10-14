// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract LeilaoMenorLanceUnico {
    struct Lance {
        address licitante;
        uint256 valor;
        string nome;
    }

    Lance[] public lances;
    address public administrador;
    uint256 public tempoFinal;
    bool public leilaoEncerrado;
    Lance public lanceVencedor;

    event LeilaoEncerrado(string nome, uint256 valor);
    event NovoLance(address licitante, uint256 valor, string nome);

    modifier somenteAntesDoFinal() {
        require(block.timestamp < tempoFinal, "Leilao ja foi encerrado");
        _;
    }

    modifier somenteDepoisDoFinal() {
        require(block.timestamp >= tempoFinal || leilaoEncerrado, "Leilao ainda esta em andamento");
        _;
    }

    constructor(uint256 _tempoLances) {
        administrador = msg.sender;
        tempoFinal = block.timestamp + _tempoLances;
    }

    function darLance(uint256 _valor, string calldata _nome) public somenteAntesDoFinal {
        require(_valor > 0, "Valor do lance deve ser maior que zero");
        lances.push(Lance(msg.sender, _valor, _nome));
        emit NovoLance(msg.sender, _valor, _nome);
    }

    function encerrarLeilao() public somenteDepoisDoFinal {
        require(!leilaoEncerrado, "Leilao ja foi encerrado");
        determinarVencedor();
        leilaoEncerrado = true;
    }

    function determinarVencedor() internal {
        // Ordenar lances por valor
        for (uint i = 0; i < lances.length - 1; i++) {
            for (uint j = i + 1; j < lances.length; j++) {
                if (lances[i].valor > lances[j].valor) {
                    Lance memory temp = lances[i];
                    lances[i] = lances[j];
                    lances[j] = temp;
                }
            }
        }

        // Determinar o menor lance unico
        bool lanceUnicoEncontrado;
        for (uint i = 0; i < lances.length; i++) {
            lanceUnicoEncontrado = true;
            for (uint j = 0; j < lances.length; j++) {
                if (i != j && lances[i].valor == lances[j].valor) {
                    lanceUnicoEncontrado = false;
                    break;
                }
            }
            if (lanceUnicoEncontrado) {
                lanceVencedor = lances[i];
                emit LeilaoEncerrado(lanceVencedor.nome, lanceVencedor.valor);
                break;
            }
        }

        // Caso nenhum lance unico seja encontrado
        if (!lanceUnicoEncontrado) {
            lanceVencedor = Lance(address(0), 0, "Nenhum vencedor");
            emit LeilaoEncerrado(lanceVencedor.nome, lanceVencedor.valor);
        }
    }

    function getNomeVencedor() public view somenteDepoisDoFinal returns (string memory) {
        require(lanceVencedor.licitante != address(0), "Nenhum vencedor determinado");
        return lanceVencedor.nome;
    }

    function imprimirVencedor() public view somenteDepoisDoFinal returns (string memory) {
        require(lanceVencedor.licitante != address(0), "Nenhum vencedor determinado");
        return string(abi.encodePacked("Vencedor: ", lanceVencedor.nome, ", Lance: ", uint2str(lanceVencedor.valor)));
    }

    function uint2str(uint256 _i) internal pure returns (string memory) {
        if (_i == 0) {
            return "0";
        }
        uint256 temp = _i;
        uint256 digits;
        while (temp != 0) {
            digits++;
            temp /= 10;
        }
        bytes memory buffer = new bytes(digits);
        while (_i != 0) {
            digits -= 1;
            buffer[digits] = bytes1(uint8(48 + _i % 10));
            _i /= 10;
        }
        return string(buffer);
    }
}
