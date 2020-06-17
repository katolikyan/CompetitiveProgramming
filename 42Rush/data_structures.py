
#                                                                              #
#                                                         :::      ::::::::    #
#    data_structures.py                                 :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: smaddox <marvin@42.fr>                     +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/10/13 15:22:23 by smaddox           #+#    #+#              #
#    Updated: 2019/10/13 23:07:58 by tkatolik         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

class stop_area:
    def __init__(self,name,stop_id):
        self.name=name
        self.stop_id=stop_id

class route:
    def __init__(self,route_id,nodes):
        self.route_id=route_id
        self.nodes=nodes
