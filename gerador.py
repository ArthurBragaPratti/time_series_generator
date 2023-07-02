class series_temporais:
    import pandas as pd
    import numpy as np

    """
    Gera um dataframe que simula séries temporais de tendência linear e possível sazonalidade. As séries temporais estão ordenadas na horizontal.\n
    Os resíduos, coeficientes angulares e interceptos são gerados com base em distribuições normais, de média e desvio padrões pré-definidos.\n
    Para o funcionamento adequado dessa classe, é necessário importar as bibliotecas Pandas e Numpy como pd e np respectivamente.\n

    size        - Quantidade de séries temporais (linhas) você deseja. (int) \n
    periodo     - Quantidade de periodos você deseja nas suas séries temporais. (int) \n
    sazonal     - Determina se as séries temporais geradas serão sazonais ou não. (bool)

    """

    #Inicializador
    def __init__(self, size, periodo, sazonal):
        self._size          = size
        self._periodo       = periodo
        self._sazonal       = sazonal
        self._x             = None
        self._e             = None
        self._angular       = None
        self._intercepto    = None
        self.dataset        = None
    

    @property
    def size(self):

        '''
        Retorna a quantidade de linhas da matriz.
        '''

        return self._size
    
    
    @property
    def periodo(self):

        ''' 
        Retorna o número de períodos das séries temporais.
        '''

        return self._periodo
    
    
    
    def e(self, media_erro, std_erro):

        ''' 
        Gera os erros normalmente distribuidos.

        media_erro - Informa a média da curva sob a qual serão gerados os erros (float). \n
        std_erro   - Intorma o desvio padrão da curva sob a qual serão gerados os erros (float).
        '''

        self._e = list(np.random.normal(media_erro, std_erro, self.periodo))


    def intercepto(self, media_intercepto, std_intercepto):

        ''' 
        Gera interceptos normalmente distribuidos.

        media_intercepto - Informa a média da curva sob a qual serão gerados os interceptos (float). \n
        std_intercepto   - Intorma o desvio padrão da curva sob a qual serão gerados os interceptos (float).
        '''

        self._intercepto = list(np.random.normal(media_intercepto, std_intercepto, self.size))

    
    def coeficiente(self, media_coe, std_coe):

        ''' 
        Gera os coeficientes normalmente distribuidos.

        media_coeficiente - Informa a média da curva sob a qual serão gerados os coeficientes (float). \n
        std_coeficiente   - Intorma o desvio padrão da curva sob a qual serão gerados os coeficientes (float).
        '''

        self._angular = list(np.random.normal(media_coe, std_coe, self.size))


    
    def x(self):

        ''' 
        Gera os períodos (colunas) da matriz, com base nos valores informados previamente.
        '''

        self._x = [i for i in range(1, self._periodo + 1)]

    
    def y(self):

        ''' 
        Gera os valores finais da função, levando em conta os coefientes, interceptos, periodos e erros.
        '''

        dataset = list()
        for a, b in zip(self._angular, self._intercepto):
            linha = list()
            for x, e in zip(self._x, self._e):
                y = (a * x) + b + e
                linha.append(y)
            
            dataset.append(linha)

        self.dataset = dataset


    def sazonalidade(self, meia_vida, elevacao, amplitude, multiplicativo):

        if self._sazonal:
            func = [amplitude * (np.cos((10 * x)/(meia_vida * np.pi)) + elevacao) for x in self._x]
            dataset = []

            if multiplicativo:
                for i in self.dataset:
                    linha = [m * n + e for m, n, e in zip(func, i, self._e)]
                    dataset.append(linha)
            else:
                for i in self.dataset:
                    linha = [m + n + e for m, n, e in zip(func, i, self._e)]
                    dataset.append(linha)

            self.dataset = dataset

        else:
            pass

    
    def gerar_dataframe(self, 
                        media_erro = 0, 
                        std_erro = 0, 
                        media_intercepto = 0, 
                        std_intercepto = 0, 
                        media_coe = 0, 
                        std_coe = 0,
                        meia_vida = 3,
                        elevacao = 1,
                        amplitude = 1,
                        multiplicativo = False):

        ''' 
        Retorna dataframe de dimensão (size x periodos) com os valores finais das séries temporais geradas. 

        media erro       - Média dos resíduos distribuidos normalmente (float).\n
        std_erro         - Desvio padrão dos resíduos distribuidos normalmente (float).\n
        media_intercepto - Média dos interceptos distribuidos normalmente (float).\n
        std_intercepto   - Desvio padrão dos interceptos distribuidos normalmente (float).\n
        media coe        - Média dos coeficientes angulares distribuidos normalmente (float).\n
        std_coe          - Desvio padrão dos coeficientes angulares distribuidos normalmente (float).\n
        meia_vida        - Quantidade de períodos que a sazonalidade demora para ir do ponto mais alto ao mais baixo (float). \n
        elevacao         - Quantas unidades a função cosseno (sazonalidade) será suspensa. Altera o ponto mais alto e o mais baixo (float). \n
        amplitude        - Fator multiplicativo para os valores de y na função cosseno. Determina o quão ampla é a nossa sazonalidade (float). \n
        multiplicativo   - Determina se a sazonalidade é aditiva ou multiplicativa (bool).
        
        '''

        self.e( media_erro = media_erro, 
                std_erro   = std_erro)
        
        self.intercepto(media_intercepto = media_intercepto,
                        std_intercepto   = std_intercepto)
        
        self.coeficiente(media_coe = media_coe,
                         std_coe   = std_coe)
        
        self.x()
        self.y()

        self.sazonalidade(meia_vida      = meia_vida,
                          elevacao       = elevacao,
                          amplitude      = amplitude,
                          multiplicativo = multiplicativo)
        
        return pd.DataFrame(self.dataset)