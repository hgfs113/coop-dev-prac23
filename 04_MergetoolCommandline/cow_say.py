import cmd
import shlex

import cowsay


EYES_PROMPT = ["xx", "XX", "oo", "OO", "oO", "Oo", "-O", "O-", "--", "^^", "щщ"]
TONGUE_PROMPTS = ["ll", "Ll", "LL", "II", "ii", "U ", " U", "[]"]


class cowsay_cmd(cmd.Cmd):
    prompt = "cowshell# "

    def do_list_cows(self, args):
        """To list all cowfiles on the current COWPATH
        Usage: list_cows [dir]
            :param dir: directory for searching cows = default: COWPATH

        """
        if len(args) > 0:
            message = cowsay.list_cows(shlex.split(args)[0])
        else:
            message = cowsay.list_cows()
        print(message)

    def do_make_bubble(self, args):
        """This is make_bubble help
        Usage: make_bubble text [-b brackets] [-W width] [-w wrap-text]
            :param brackets: cowsay / cowthink = defult: cowsay
            :param width: int = defult: 40
            :param wrap-text: bool = defult: True

        """
        text, *options = shlex.split(args)
        brackets = cowsay.THOUGHT_OPTIONS["cowsay"]
        width = 40
        wrap_text = True
        if options:
            assert len(options) % 2 == 0, "Bad parameters"
            for opt, val in zip(options[::2], options[1::2]):
                if opt == "-b":
                    brackets = cowsay.THOUGHT_OPTIONS[val]
                elif opt == "-W":
                    width = int(val)
                elif opt == "-w":
                    wrap_text = val.lower() == "true" or val.lower() == "y" or \
                            val.lower() == "yes" or val.lower() == "da"
        print(cowsay.make_bubble(text, brackets=brackets, width=width, wrap_text=wrap_text))

    def complete_make_bubble(self, text, line, begidx, endidx):
        args = shlex.split(line)
        if len(args) < 3:
            return []
        if begidx != endidx:
            control_key = args[-2]
        else:
            control_key = args[-1]
        print(control_key)
        if control_key == "-b":
            prompts = ["cowsay", "cowthink"]
        elif control_key == "-w":
            prompts = ["True", "true", "yes", "Yes", "Da", "da", "False", "false", "No", "no", "Net", "net"]
        else:
            return []

        return list(filter(lambda x: x.startswith(text), prompts))

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
        text, named_params = self._get_cow_do_opts(args)
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
        text, named_params  = self._get_cow_do_opts(args)
        print(cowsay.cowthink(text, **named_params))

    @staticmethod
    def _get_cow_do_opts(args):
        """Iternal function for params handling

        """
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

    def complete_cowsay(self, text, line, begidx, endidx):
        return self._complete_cow_star(text, line, begidx, endidx)

    def complete_cowthink(self, text, line, begidx, endidx):
        return self._complete_cow_star(text, line, begidx, endidx)

    @staticmethod
    def _complete_cow_star(text, line, begidx, endidx):
        line = shlex.split(line)
        if len(args) < 3:
            return []
        if begidx != endidx:
            control_key = args[-2]
        else:
            control_key = args[-1]
        if control_key == "-e":
            prompts = EYES_PROMPT
        elif control_key == "-T":
            prompts = TONGUE_PROMPTS
        elif control_key == "-f":
            prompts = cowsay.list_cows()
        else:
            return []

        return list(filter(lambda x: x.startswith(text), prompts))


if __name__ == "__main__":
    cowsay_cmd().cmdloop()
