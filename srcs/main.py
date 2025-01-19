from srcs.modules.managers.ca_core import CaCore
from srcs.modules.managers.ca_test import ca_test

from srcs.modules.managers.ca_register import CaTopRegister
from srcs.modules.managers.ca_configurator import CaTopConfigurator

from srcs.modules.tables.ca_kh import CaKh, CaTopKh
from srcs.modules.tables.ca_kf import CaKf, CaTopKf
from srcs.modules.tables.ca_tgpsi_ch import CaTgPsiCh, CaTopTgPsiCh
from srcs.modules.tables.ca_tgpsi_unch import CaTgPsiUnCh, CaTopTgPsiUnCh


from srcs.modules.processors.ca_handler import CaHandler, CaTopHandler
from srcs.modules.processors.ca_runner import CaTopRunner


def main():
    """
    Entry point of the application.
    Initializes and runs the core application.
    """
    
    core = CaCore()
    core.register.add_command(["test"], ca_test)
    
    top_register = CaTopRegister(core)
    core.register.add_command(["man", "help"], top_register.help_command)
    core.register.add_command("cfg.gen", top_register.generate_config_file)
    
    top_configurator = CaTopConfigurator(core)
    core.register.add_command("cfg.find", top_configurator.find_config_file)
    core.register.add_command("cfg.upload", top_configurator.upload)
    core.register.add_command("cfg.download", top_configurator.download)
    
    kH = CaKh()
    top_kH = CaTopKh(kH)
    core.register.add_command("kH.print", top_kH.print)

    kF = CaKf()
    top_kF = CaTopKf(kF)
    core.register.add_command("kF.print", top_kF.print)

    tgpsi_ch = CaTgPsiCh()
    top_tgpsi_ch = CaTopTgPsiCh(tgpsi_ch)
    core.register.add_command("tgCh.print", top_tgpsi_ch.print)

    tgpsi_unch = CaTgPsiUnCh()
    top_tgpsi_unch = CaTopTgPsiUnCh(tgpsi_unch)
    core.register.add_command("tgUnCh.print", top_tgpsi_unch.print)

    data_handler = CaHandler()
    top_data_handler = CaTopHandler(core, data_handler)
    core.register.add_command("hand.extract", top_data_handler.extract)
    core.register.add_command("hand.execute", top_data_handler.execute)
    core.register.add_command("hand.read", top_data_handler.read)
    

    top_runner = CaTopRunner(core, top_configurator, top_data_handler)
    core.register.add_command("run", top_runner.main)
    
    core.run()


if __name__ == "__main__":
    main()