

def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()
    
    if lowered == '':
        return 'okay...'
    elif lowered == 'opgg':
        return "OPGG"
    else:
        return "william is gay"