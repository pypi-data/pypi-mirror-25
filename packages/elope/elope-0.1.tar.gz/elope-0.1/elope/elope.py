def elvis(val):
  try:
    if val:
      return True
    else:
      raise Exception
  except Exception:
    return False
