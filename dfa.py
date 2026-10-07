class LogDFA:

    def __init__(self):
        # Starting state
        self.state = "S0"

        # Suspicious activity flag
        self.suspicious = False

    def process(self, level):

        # ==========================================
        # S0 - NORMAL STATE
        # ==========================================

        if self.state == "S0":

            if level == "ERROR":
                self.state = "S1"
            else:
                self.state = "S0"


        # ==========================================
        # S1 - ONE CONSECUTIVE ERROR
        # ==========================================

        elif self.state == "S1":

            if level == "ERROR":
                self.state = "S2"
            else:
                self.state = "S0"


        # ==========================================
        # S2 - TWO CONSECUTIVE ERRORS
        # ==========================================

        elif self.state == "S2":

            if level == "ERROR":
                self.state = "S3"
                self.suspicious = True
            else:
                self.state = "S0"


        # ==========================================
        # S3 - SUSPICIOUS STATE
        # ==========================================

        elif self.state == "S3":

            self.state = "S3"

        return self.state


    # ==============================================
    # CHECK SUSPICIOUS ACTIVITY
    # ==============================================

    def is_suspicious(self):

        return self.suspicious