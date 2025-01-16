from srcs.modules.managers.ca_core import CaCore

from srcs.modules.tables.ca_kh import CaKh
from srcs.modules.tables.ca_kf import CaKf
from srcs.modules.tables.ca_tgpsi_unch import CaTgPsiUnCh
from srcs.modules.tables.ca_tgpsi_ch import CaTgPsiCh

from srcs.modules.analyzers.ca_data_handler import CaDataHandler, CaTopDataHandler
from srcs.modules.managers.ca_configurator import CaTopConfigurator

def main():
    """
    Entry point of the application.
    Initializes and runs the core application.
    """
    core = CaCore()

    top_configurator = CaTopConfigurator(core)
    core.register.add_command("cfg.load-gen", top_configurator.load_conf_and_generate_conf)

    kH = CaKh()
    core.register.add_command("kH.print", kH.print)

    kF = CaKf()
    core.register.add_command("kF.print", kF.print)

    tgpsi_ch = CaTgPsiCh()
    core.register.add_command("tgCh.print", tgpsi_ch.print)

    tgpsi_unch = CaTgPsiUnCh()
    core.register.add_command("tgUnCh.print", tgpsi_unch.print)

    data_handler = CaDataHandler()
    core.register.add_command("handler.execute", data_handler.execute)

    top_data_handler = CaTopDataHandler(core, data_handler, print_cmds=["handler.execute"])
    core.register.add_command("handler.print", top_data_handler.print)



    core.run()


if __name__ == "__main__":
    main()