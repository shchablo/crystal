from srcs.modules.managers.ca_core import CaCore

from srcs.modules.tables.ca_table_kh import CaTableKh
from srcs.modules.tables.ca_table_kf import CaTableKf
from srcs.modules.tables.ca_table_tgpsi_ch import CaTableTgPsiCh
from srcs.modules.tables.ca_table_tgpsi_unch import CaTableTgPsiUnCh

def main():
    """
    Entry point of the application.
    Initializes and runs the core application.
    """
    core = CaCore()

    table_kH = CaTableKh()
    core.register.add_command("kh.p", table_kH.print)
    core.register.add_command("kh.csv", table_kH.save_to_csv_with_steps)
    
    table_kF = CaTableKf()
    core.register.add_command("kf.p", table_kF.print)
    core.register.add_command("kf.csv", table_kF.save_to_csv_with_steps)

    table_tgpsi_ch = CaTableTgPsiCh()
    core.register.add_command("tgPsi.ch.p", table_tgpsi_ch.print)
    core.register.add_command("tgPsi.ch.csv", table_tgpsi_ch.save_to_csv_with_steps)
    
    table_tgpsi_unch = CaTableTgPsiUnCh()
    core.register.add_command("tgPsi.unch.p", table_tgpsi_unch.print)
    core.register.add_command("tgPsi.unch.csv", table_tgpsi_unch.save_to_csv_with_steps)

    core.run()


if __name__ == "__main__":
    main()