import cmd
import shlex

import cowsay


class cowsay_cmd(cmd.Cmd):
    prompt = "cowshell# "

    def do_list_cows(self, args):
        """To list all cowfiles on the current COWPATH
        Usage: list_cows [dir]

        """
        if len(args) > 0:
            message = cowsay.list_cows(shlex.split(args)[0])
        else:
            message = cowsay.list_cows()
        print(message)

    def do_make_bubble(self, args):
        """This is make_bubble help
        Usage: make_bubble text
            [param: --brackets: cowsay / cowthink = defult: cowsay]
            [param: --width: int = defult: 40]
            [param: --wrap-text: bool = defult: True]
        """
        text, *options = shlex.split(args)
        brackets = cowsay.THOUGHT_OPTIONS["cowsay"]
        width = 40
        wrap_text = True
        if options:
            assert len(options) % 2 == 0, "Bad parameters"
            for opt, val in zip(options[::2], options[1::2]):
                if opt == "--brackets":
                    brackets = cowsay.THOUGHT_OPTIONS[val]
                elif opt == "--width":
                    width = int(val)
                elif opt == "--wrap-text":
                    wrap_text = val.lower() == "true" or val.lower() == "y" or \
                            val.lower() == "yes" or val.lower() == "da"
        print(cowsay.make_bubble(text, brackets=brackets, width=width, wrap_text=wrap_text))

    def do_cowsay(self, args):
        """Similar to the cowsay command. Parameters are listed with their
        corresponding options in the cowsay command. Returns the resulting cowsay
        string
        Usage: cowsay text [-e eyes] [-T tongue] [-f cow]
        :param text: The message to be displayed
        :param eyes: eye_string = default: 'oo'
        :param tongue: tongue_string = default: '  '
        :param cow: the available cows can be found by calling list_cows = default: 'default'

        """
        text, named_params = self.get_cow_do_opts(args)
        print(cowsay.cowsay(text, **named_params))

    def do_cowthink(self, args):
        """Similar to the cowsay command. Parameters are listed with their
        corresponding options in the cowsay command. Returns the resulting cowsay
        string
        Usage: cowsay text [-e eyes] [-T tongue] [-f cow]
        :param text: The message to be displayed
        :param eyes: eye_string = default: 'oo'
        :param tongue: tongue_string = default: '  '
        :param cow: the available cows can be found by calling list_cows = default: 'default'
        
        """
        text, named_params  = self.get_cow_do_opts(args)
        print(cowsay.cowthink(text, **named_params))

    @staticmethod
    def get_cow_do_opts(args):
        text, *options = shlex.split(args)
        named_params = {"cow": "default", "eyes": "oo", "tongue": "  "}
        if options:
            assert len(options) % 2 == 0, "Bad parameters"
            for opt, val in zip(options[::2], options[1::2]):
                if opt == "-e":
                    named_params["eyes"] = val[:2]
                elif opt == "-T":
                    named_params["tongue"] = val[:2]
                elif opt == "-f":
                    assert val in cowsay.list_cows(), "Invalid cow"
                    named_params["cow"] = val
        return text, named_params

if __name__ == "__main__":
    cowsay_cmd(completekey="k").cmdloop()
