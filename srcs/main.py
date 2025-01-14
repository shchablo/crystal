from srcs.modules.managers.ca_core import CaCore

from srcs.modules.tables.ca_kh import CaKh
from srcs.modules.tables.ca_kf import CaKf
from srcs.modules.tables.ca_tgpsi_ch import CaTgPsiCh
from srcs.modules.tables.ca_tgpsi_unch import CaTgPsiUnCh

def main():
    """
    Entry point of the application.
    Initializes and runs the core application.
    """
    core = CaCore()

    kH = CaKh()
    core.register.add_command("kh.p", kH.print)
    
    kF = CaKf()
    core.register.add_command("kf.p", kF.print)

    tgpsi_ch = CaTgPsiCh()
    core.register.add_command("tgpsi.ch.p", tgpsi_ch.print)
    
    tgpsi_unch = CaTgPsiUnCh()
    core.register.add_command("tgpsi.unch.p", tgpsi_unch.print)

    core.run()


if __name__ == "__main__":
    main()