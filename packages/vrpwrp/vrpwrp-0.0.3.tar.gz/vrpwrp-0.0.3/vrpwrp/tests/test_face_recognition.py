#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import vrpwrp.tools.embedding as EMB
import vrpwrp.wrappers.face_recognition as FACEREC

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except:
    NUMPY_AVAILABLE = False

__author__ = 'Iván de Paz Centeno'


Embedding = EMB.Embedding
FaceRecognition = FACEREC.FaceRecognition

class TestFaceRecognition(unittest.TestCase):
    """
    Unit tests for the class FaceRecognition
    """
    def test_get_embedding_from_face_file(self):
        """
        Tests the extraction of an embedding from a file.
        """
        face_recognition = FaceRecognition()
        embedding = face_recognition.get_embeddings_from_file("vrpwrp/examples/subject3_3.jpg")
        self.assertTrue(type(embedding) is Embedding)

    def test_get_embeddings_distances_with_numpy(self):
        """
        Tests whether the face recognition can get massive embeddings distances with numpy.
        :return:
        """
        if NUMPY_AVAILABLE:
            EMB.NUMPY_LOADED = True
            FACEREC.NUMPY_AVAILABLE = True

            emb1 = Embedding("[ 0.0158451  -0.10712819  0.03863023 -0.03482883 -0.0824572   0.14168985 -0.09636037  0.19106716 -0.02492222  0.14210707 -0.01116645 -0.02843223  0.11468598  0.05238573 -0.07595719  0.02790567  0.08421595 -0.02046278  0.11567297 -0.04182892  0.04587755  0.06748006  0.16458501  0.10763472 -0.129269   -0.06824924  0.04409041  0.02964318 -0.038321   -0.0219803 -0.18692227  0.1463057  -0.01780165 -0.04693119  0.14571658 -0.07666277 -0.00090835  0.10656494  0.05686795 -0.00907048 -0.02277039 -0.04237205  0.05263669 -0.0703985  -0.0910216   0.00665178  0.18419671 -0.16580425  0.10267366  0.031062   -0.06323228  0.01181003  0.10920595 -0.06083095  0.00112445 -0.05585416 -0.0517714  -0.01066756 -0.10822885 -0.02711556 -0.04817014  0.09187203 -0.0778175   0.01809014  0.06878112  0.01106403  0.22116356  0.11943804  0.01060378  0.1570053   0.01113725  0.18296902  0.14617686  0.09622544  0.03298299  0.01186595 -0.0497611  -0.02599285 -0.0180933  -0.04265066  0.01374123 -0.10514697  0.04546366 -0.01592954  0.02338098  0.04642355  0.04885073 -0.14540456 -0.03893084 -0.0271441  0.14776005  0.12446663 -0.19740807  0.00212946  0.10007296  0.14576022  0.00851103  0.14883877 -0.09683412 -0.153027    0.00841949 -0.02203198 -0.08422936 -0.08729295  0.02269308  0.03118366  0.03445914 -0.05186762  0.11506347  0.0202589  -0.05157725  0.05116833 -0.03643497  0.09496777 -0.13442048 -0.09157681 -0.03467375 -0.08306352 -0.0041221  -0.06054366 -0.11433879 -0.09384206 -0.04435525  0.08906819  0.1288448  -0.0818419  0.09191026 -0.0867103 ]")
            embs_who = [Embedding("[-0.0{}  0.02188188  0.08280295  0.03783304 -0.01933468  0.03775278  0.0931235  -0.02352021  0.06010089  0.00089534 -0.08144676  0.09437996  0.05528472 -0.08782918  0.02388905 -0.03227656  0.07940276  0.03790136  0.04989427  0.00074208  0.00774619 -0.01066396  0.03521054 -0.08510022  0.04805138  0.04995364  0.03496696  0.07999235  0.05855429  0.12293658 -0.06525446  0.0350027  -0.05571594 -0.11703292 -0.00822121 -0.10753039  0.04798333  0.03394997  0.01345209 -0.06920611  0.03951461  0.08906944  0.05040617  0.1595071   0.15870747  0.138016   -0.03988503 -0.16869368 -0.15910695  0.16755092 -0.08412354  0.06929413 -0.00696136 -0.01855957 -0.09980983  0.03130403  0.16348867 -0.02478264  0.01473257 -0.12003439  0.04467747  0.15205432 -0.05045622 -0.04657688 -0.10278953  0.05550895 -0.00257586 -0.07990343 -0.15728523 -0.15495953 -0.06836285 -0.02878328  0.11981599 -0.17039472  0.10333136  0.02417856 -0.12819001 -0.06802902 -0.00152423 -0.01483421  0.08994423  0.10568022 -0.08645283 -0.14509805 -0.02411678 -0.02262853  0.0802597   0.19059512 -0.03327667  0.09519654 -0.09965424  0.08643778 -0.02620865 -0.08090184  0.03863079  0.00783935  0.05062248 -0.13768932 -0.15904306 -0.06786504  0.09602615  0.01017415 -0.02701177 -0.20418924  0.0419284  -0.00059234  0.00649145  0.00732872  0.24222451  0.08798994 -0.06830025 -0.00691073  0.06116113  0.0321093 -0.06775422 -0.030848   -0.13546759  0.02979624  0.12392963 -0.0808115  0.03381168 -0.01160022  0.11621546  0.03767033  0.20028599 -0.108992  0.142269    0.01581674]".format(x)) for x in range(100)]

            face_recognition = FaceRecognition()
            distances = face_recognition.get_embeddings_distances(emb1, embs_who)
            self.assertTrue(len(distances) == len(embs_who))
        else:
            self.assertTrue(True)

    def test_get_embeddings_distances_without_numpy(self):
        """
        Tests whether the face recognition can get massive embeddings distances with numpy.
        :return:
        """
        EMB.NUMPY_LOADED = False
        FACEREC.NUMPY_AVAILABLE = False

        emb1 = Embedding("[ 0.0158451  -0.10712819  0.03863023 -0.03482883 -0.0824572   0.14168985 -0.09636037  0.19106716 -0.02492222  0.14210707 -0.01116645 -0.02843223  0.11468598  0.05238573 -0.07595719  0.02790567  0.08421595 -0.02046278  0.11567297 -0.04182892  0.04587755  0.06748006  0.16458501  0.10763472 -0.129269   -0.06824924  0.04409041  0.02964318 -0.038321   -0.0219803 -0.18692227  0.1463057  -0.01780165 -0.04693119  0.14571658 -0.07666277 -0.00090835  0.10656494  0.05686795 -0.00907048 -0.02277039 -0.04237205  0.05263669 -0.0703985  -0.0910216   0.00665178  0.18419671 -0.16580425  0.10267366  0.031062   -0.06323228  0.01181003  0.10920595 -0.06083095  0.00112445 -0.05585416 -0.0517714  -0.01066756 -0.10822885 -0.02711556 -0.04817014  0.09187203 -0.0778175   0.01809014  0.06878112  0.01106403  0.22116356  0.11943804  0.01060378  0.1570053   0.01113725  0.18296902  0.14617686  0.09622544  0.03298299  0.01186595 -0.0497611  -0.02599285 -0.0180933  -0.04265066  0.01374123 -0.10514697  0.04546366 -0.01592954  0.02338098  0.04642355  0.04885073 -0.14540456 -0.03893084 -0.0271441  0.14776005  0.12446663 -0.19740807  0.00212946  0.10007296  0.14576022  0.00851103  0.14883877 -0.09683412 -0.153027    0.00841949 -0.02203198 -0.08422936 -0.08729295  0.02269308  0.03118366  0.03445914 -0.05186762  0.11506347  0.0202589  -0.05157725  0.05116833 -0.03643497  0.09496777 -0.13442048 -0.09157681 -0.03467375 -0.08306352 -0.0041221  -0.06054366 -0.11433879 -0.09384206 -0.04435525  0.08906819  0.1288448  -0.0818419  0.09191026 -0.0867103 ]")
        embs_who = [Embedding("[-0.0{}  0.02188188  0.08280295  0.03783304 -0.01933468  0.03775278  0.0931235  -0.02352021  0.06010089  0.00089534 -0.08144676  0.09437996  0.05528472 -0.08782918  0.02388905 -0.03227656  0.07940276  0.03790136  0.04989427  0.00074208  0.00774619 -0.01066396  0.03521054 -0.08510022  0.04805138  0.04995364  0.03496696  0.07999235  0.05855429  0.12293658 -0.06525446  0.0350027  -0.05571594 -0.11703292 -0.00822121 -0.10753039  0.04798333  0.03394997  0.01345209 -0.06920611  0.03951461  0.08906944  0.05040617  0.1595071   0.15870747  0.138016   -0.03988503 -0.16869368 -0.15910695  0.16755092 -0.08412354  0.06929413 -0.00696136 -0.01855957 -0.09980983  0.03130403  0.16348867 -0.02478264  0.01473257 -0.12003439  0.04467747  0.15205432 -0.05045622 -0.04657688 -0.10278953  0.05550895 -0.00257586 -0.07990343 -0.15728523 -0.15495953 -0.06836285 -0.02878328  0.11981599 -0.17039472  0.10333136  0.02417856 -0.12819001 -0.06802902 -0.00152423 -0.01483421  0.08994423  0.10568022 -0.08645283 -0.14509805 -0.02411678 -0.02262853  0.0802597   0.19059512 -0.03327667  0.09519654 -0.09965424  0.08643778 -0.02620865 -0.08090184  0.03863079  0.00783935  0.05062248 -0.13768932 -0.15904306 -0.06786504  0.09602615  0.01017415 -0.02701177 -0.20418924  0.0419284  -0.00059234  0.00649145  0.00732872  0.24222451  0.08798994 -0.06830025 -0.00691073  0.06116113  0.0321093 -0.06775422 -0.030848   -0.13546759  0.02979624  0.12392963 -0.0808115  0.03381168 -0.01160022  0.11621546  0.03767033  0.20028599 -0.108992  0.142269    0.01581674]".format(x)) for x in range(100)]

        face_recognition = FaceRecognition()
        distances = face_recognition.get_embeddings_distances(emb1, embs_who)
        self.assertTrue(len(distances) == len(embs_who))


if __name__ == '__main__':
    unittest.main()
