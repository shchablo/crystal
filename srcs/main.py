from srcs.modules.managers.ca_core import CaCore
from srcs.modules.managers.ca_test import ca_test

from srcs.modules.managers.ca_register import CaTopRegister
from srcs.modules.managers.ca_configurator import CaTopConfigurator

from srcs.modules.tables.ca_kh import CaKh, CaTopKh
from srcs.modules.tables.ca_kf import CaKf, CaTopKf
from srcs.modules.tables.ca_tgpsi_ch import CaTgPsiCh, CaTopTgPsiCh
from srcs.modules.tables.ca_tgpsi_unch import CaTgPsiUnCh, CaTopTgPsiUnCh


from srcs.modules.processors.ca_handler import CaHandler, CaTopHandler
from srcs.modules.processors.ca_calculator import CaCalculator, CaTopCalculator
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
    
    kh = CaKh()
    top_kh = CaTopKh(kh)
    core.register.add_command("kh.print", top_kh.print)

    kf = CaKf()
    top_kf = CaTopKf(kf)
    core.register.add_command("kf.print", top_kf.print)

    tgpsi_ch = CaTgPsiCh()
    top_tgpsi_ch = CaTopTgPsiCh(tgpsi_ch)
    core.register.add_command("tg.ch.print", top_tgpsi_ch.print)

    tgpsi_unch = CaTgPsiUnCh()
    top_tgpsi_unch = CaTopTgPsiUnCh(tgpsi_unch)
    core.register.add_command("tg.unch.print", top_tgpsi_unch.print)

    handler = CaHandler()
    top_handler = CaTopHandler(core, handler)
    core.register.add_command("hand.extract", top_handler.extract)
    core.register.add_command("hand.execute", top_handler.execute)
    core.register.add_command("hand.read", top_handler.read)
    core.register.add_command("hand.print", top_handler.print)
    

    calculator = CaCalculator(handler, kh, kf, tgpsi_ch, tgpsi_unch)
    top_calculator = CaTopCalculator(core, calculator)
    core.register.add_command("calc.input", top_calculator.process_inputs)
    core.register.add_command("calc.profiles", top_calculator.process_profiles)


    top_runner = CaTopRunner(core, top_configurator, top_handler, top_calculator)
    core.register.add_command("run", top_runner.main)
    
    core.run()


if __name__ == "__main__":
    main()