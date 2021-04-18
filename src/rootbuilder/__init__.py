###############################################################################
#                                                                             #
#                  Copyright(C) 2020 Vaneixus Prime                           #
#                                                                             #
#  Root Builder is free software: you can redistribute it and/or modify       #
#  it under the terms of the GNU General Public License as published by       #
#  the Free Software Foundation, either version 3 of the License, or          #
#  any later version.                                                         #
#                                                                             #
#  Root Builder is distributed in the hope that it will be useful, but        #
#  WITHOUT ANY WARRANTY without even the implied warranty of MERCHANTABILITY  #
#  or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License   #
#  for more details.                                                          #
#                                                                             #
#  You should have received a copy of the GNU General Public License          #
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.     #
#                                                                             #
###############################################################################


from . import rootbuilder_launcher

def createPlugins():
    return [rootbuilder_launcher.RootBuilder()]