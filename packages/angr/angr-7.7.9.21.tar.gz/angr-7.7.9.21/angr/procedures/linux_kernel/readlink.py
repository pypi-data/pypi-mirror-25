import angr

class readlink(angr.SimProcedure):
    def run(self, in_ptr, out_ptr, out_size):
        if self.state.mem[in_ptr].string.concrete == '/proc/self/exe':
            pass
        else:
            raise angr.errors.SimProcedureError
