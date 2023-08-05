
class ArithmeticSkill:

    def __init__(self, tts_service=None):
        """ Initialisation.
        :param db: the json database.
        :param tts_service: A TTS service, i.e. an object which has a
                                                `speak(text)` method for speaking the result.
        """
        self.tts_service = tts_service

    def solve(self, numberA, operator, numberB):

        result = None

        if numberA is not None and numberB is not None:
            if operator == 'plus':
                result = numberA + numberB
            elif operator == 'minus':
                result = numberA - numberB
            elif operator == 'multiplied by':
                result = numberA * numberB
            elif operator == 'divided by':
                result = numberA / numberB
        return result

    def solve_and_say(self, numberA, numberB, operator):
        print('solve and say {} {} {}'.format(numberA, operator, numberB))
        # __log('solve and say {} {} {}'.format(numberA,numberB,operator))
        result = self.solve(numberA, operator, numberB)

        print(result)
        if result is not None:
            if self.tts_service:
                print('have TTdS')
                print("{} {} {} is {}".format(numberA, operator, numberB, result))
                self.tts_service.speak("{} {} {} is {}".format(numberA, operator, numberB, result))
