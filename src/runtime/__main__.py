from piecewalker import ned2_provider

if __name__ == "__main__":
    ned2 = ned2_provider.get_ned2()

    ned2.move(from_idx=None, to_idx=None, back_to_idle=False)
    ned2.move(from_idx=None, to_idx=None, back_to_idle=False)
    ned2.move(from_idx=None, to_idx=None, back_to_idle=False)
    ned2.move(from_idx=None, to_idx=None, back_to_idle=False)
    ned2.move(from_idx=None, to_idx=None, back_to_idle=False)
    ned2.move(from_idx=None, to_idx=None, back_to_idle=False)
    ned2.move(from_idx=None, to_idx=None, back_to_idle=False)
    ned2.move(from_idx=None, to_idx=None, back_to_idle=False)
    ned2.move(from_idx=None, to_idx=None, back_to_idle=True)

    ned2_provider.close_ned2()
