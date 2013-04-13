class TablatureArrangement(object):

    def __call__(self, num_frets, tuning, capo, mei):
        '''
        Your tablature arrangement algorithm should be placed here.
        Append string and fret estimates to each note event in the given MEI file.
        Return the MEI file as a string. Robotaba will take care of writing the 
        file in the proper place and entering the appropriate information in the database.

        PARAMETERS
        ----------
        num_frets (int): number of frets on the user's guitar
        tuning (String): string of the pitches of open plucks on the user's guitar or identifier
            e.g., 'E4 B3 G3 D3 A2 E2' or 'standard'
        capo (int): fret number the capo is on. 0 if no capo is used.
        mei (string): contents of the mei file as a string
        '''

        return mei_str
