# @specre 01KJXTG35F6TPQJYNHA9TFPGAE
# raised when an object or collection tries to decorate itself,
# without having an inferrable decorator
class UninferrableDecoratorError < NameError
end
