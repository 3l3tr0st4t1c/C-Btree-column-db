import ctypes
import os

# 1. Carrega a biblioteca dinâmica compilada em C
_path = os.path.abspath("./libmongoldb.so")
_lib = ctypes.CDLL(_path)

# 2. Definições de Constantes de Tamanho e Criptografia
TAMANHO_PAD_CLIENTE = 3972
TAMANHO_PAD_FINANCEIRO = 4079
TAMANHO_PAD_ENTREGA = 3626
TAMANHO_PAD_STATUS = 4075

# 3. Mapeamento das Estruturas Colunares da API do iFood
class ColunaCliente(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("idCliente", ctypes.c_uint32),
        ("nome", ctypes.c_char * 100),
        ("telefone", ctypes.c_char * 20),
        ("padding", ctypes.c_uint8 * TAMANHO_PAD_CLIENTE)
    ]

class ColunaFinanceiro(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("valorBruto", ctypes.c_int64),
        ("taxaEntrega", ctypes.c_int64),
        ("metodoPagamento", ctypes.c_uint8),
        ("padding", ctypes.c_uint8 * TAMANHO_PAD_FINANCEIRO)
    ]

class ColunaEntrega(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("bairro", ctypes.c_char * 50),
        ("logradouro", ctypes.c_char * 150),
        ("numero", ctypes.c_char * 20),
        ("complemento", ctypes.c_char * 100),
        ("referencia", ctypes.c_char * 150),
        ("padding", ctypes.c_uint8 * TAMANHO_PAD_ENTREGA)
    ]

class ColunaStatus(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("displayID", ctypes.c_int),
        ("status", ctypes.c_uint8),
        ("momentoEntrada", ctypes.c_int64),
        ("momentoDespacho", ctypes.c_int64),
        ("padding", ctypes.c_uint8 * TAMANHO_PAD_STATUS)
    ]

class SessaoCripto(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("cliente_publica", ctypes.c_uint8 * 32),
        ("cliente_secreta", ctypes.c_uint8 * 32),
        ("servidor_publica", ctypes.c_uint8 * 32),
        ("servidor_secreta", ctypes.c_uint8 * 32),
        ("chave_tx", ctypes.c_uint8 * 32),
        ("chave_rx", ctypes.c_uint8 * 32),
        ("nonce", ctypes.c_uint8 * 12),
        ("chave_local", ctypes.c_uint8 * 32)
    ]

# 4. Configuração das Assinaturas das Funções Nativas do Core
_lib.Inicializar_Banco.argtypes = [ctypes.c_char_p]
_lib.Inicializar_Banco.restype = ctypes.c_int

_lib.Inserir_Pedido.argtypes = [
    ctypes.c_char_p,
    ctypes.pointer(ColunaCliente),
    ctypes.pointer(ColunaFinanceiro),
    ctypes.pointer(ColunaEntrega),
    ctypes.pointer(ColunaStatus)
]
_lib.Inserir_Pedido.restype = ctypes.c_int

_lib.Gravar_Buffer_Offline.argtypes = [
    ctypes.c_uint8,
    ctypes.pointer(ColunaCliente),
    ctypes.pointer(ColunaFinanceiro),
    ctypes.pointer(ColunaEntrega),
    ctypes.pointer(ColunaStatus),
    ctypes.pointer(SessaoCripto)
]
_lib.Gravar_Buffer_Offline.restype = ctypes.c_int

_lib.Preparar_Carga_Criptografada.argtypes = []
_lib.Preparar_Carga_Criptografada.restype = None

_lib.Desmonte.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
_lib.Desmonte.restype = ctypes.c_int

_lib.Inicializar_Seguranca.argtypes = [ctypes.pointer(SessaoCripto)]
_lib.Inicializar_Seguranca.restype = ctypes.c_int


# 5. Interface Limpa de Alto Nível para o Time da Interface Gráfica
class MongolDB:
    def __init__(self, nome_banco="banco.dat"):
        self.db_name = nome_banco.encode('utf-8')
        _lib.Inicializar_Banco(self.db_name)

        # Mantém a sessão de segurança ativa na RAM da aplicação
        self.sessao = SessaoCripto()
        _lib.Inicializar_Seguranca(ctypes.byref(self.sessao))

    def salvar_pedido_online(self, id_cliente, nome, telefone, valor_bruto_centavos, taxa_entrega_centavos, metodo_pagto, display_id, status, bairro, logradouro, numero, compl="", ref=""):
        """ Função para quando o dashboard tem conexão direta com o servidor """
        c = ColunaCliente(idCliente=id_cliente, nome=nome.encode('utf-8'), telefone=telefone.encode('utf-8'))
        f = ColunaFinanceiro(valorBruto=valor_bruto_centavos, taxaEntrega=taxa_entrega_centavos, metodoPagamento=metodo_pagto)
        e = ColunaEntrega(bairro=bairro.encode('utf-8'), logradouro=logradouro.encode('utf-8'), numero=numero.encode('utf-8'), complemento=compl.encode('utf-8'), referencia=ref.encode('utf-8'))
        s = ColunaStatus(displayID=display_id, status=status, momentoEntrada=0, momentoDespacho=0)

        return _lib.Inserir_Pedido(self.db_name, ctypes.byref(c), ctypes.byref(f), ctypes.byref(e), ctypes.byref(s))

    def salvar_pedido_offline(self, operacao, id_cliente, nome, telefone, valor_bruto_centavos, taxa_entrega_centavos, metodo_pagto, display_id, status, bairro, logradouro, numero, compl="", ref=""):
        """ Função para quando a API do iFood cai ou perde a rede (Salva encriptado localmente) """
        c = ColunaCliente(idCliente=id_cliente, nome=nome.encode('utf-8'), telefone=telefone.encode('utf-8'))
        f = ColunaFinanceiro(valorBruto=valor_bruto_centavos, taxaEntrega=taxa_entrega_centavos, metodoPagamento=metodo_pagto)
        e = ColunaEntrega(bairro=bairro.encode('utf-8'), logradouro=logradouro.encode('utf-8'), numero=numero.encode('utf-8'), complemento=compl.encode('utf-8'), referencia=ref.encode('utf-8'))
        s = ColunaStatus(displayID=display_id, status=status, momentoEntrada=0, momentoDespacho=0)

        return _lib.Gravar_Buffer_Offline(operacao, ctypes.byref(c), ctypes.byref(f), ctypes.byref(e), ctypes.byref(s), ctypes.byref(self.sessao))

    def disparar_sincronizacao(self):
        """ Executa a transição AES local -> Curve25519 de rede """
        _lib.Preparar_Carga_Criptografada()

    def processar_carga_no_servidor(self, arquivo_enc):
        """ Executado no core do servidor para reidratar a Árvore B colunar """
        return _lib.Desmonte(arquivo_enc.encode('utf-8'), self.db_name)
