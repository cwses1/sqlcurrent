class StringLiteralFormatter ():

    @staticmethod
    def format (tokenLiteral:str) -> str:
        return tokenLiteral.strip('\'')
