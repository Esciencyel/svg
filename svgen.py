import xml.etree.ElementTree as ET
import cairosvg

class Svg:
  def __init__(self):
    pass
  
  def setProperties(self):
    pass
  
  def readProperties(self):
    pass
  
  def resetIDs(self):
    pass
  
  def load(self):
    pass
  
  def save(self, erase=False):
    pass
  
  def insert(self, other, z='top', keepWorking=True, override=False):
    # Charger le fichier source
    other_tree= ET.parse(other)
    other_root = other_tree.getroot()

    # Insérer le contenu du fichier source dans le fichier destination
    for element in other_root:
        self.root.append(element)

    # Enregistrer le fichier modifié
    name = self.name
    if not erase:
      name = self.name.replace('.svg', '_merged.svg')
    self.tree.write(name)
      
  def resize(self, width, height=None):
    # Charger le fichier SVG
    with open(self.path, 'r') as inputf:
        svg_data = inputf.read()
        
    current_width, current_height = self.getDimensions(self)
        
    if not height:
      height = (width/current_width) * current_height

    # Redimensionner le SVG avec le même ratio
    return cairosvg.transform.resize(svg_data, width=width, height=height)
    
  def getElements(self, criteria, name):
    pass
  
  def getElementByClass(self, _class: str):
    pass
  
  def getElementByID(self, _id: str):
    pass
  
  def getElementByTag(self, _tag:str):
    pass
  
  def groupElementByClass(self, _class):
    pass
  
  def groupElementByID(self, _id):
    pass
  
  def groupElementByTag(self, _tag):
    pass
 
class Layer(Svg):
  def __init__(self):
    super().__init__(self)
    

class ImageToSvg:
  def __init__(self, svg_file_path):
    self.path = svg_file_path
    self.tree = ET.parse(self.path)
    self.root = self.tree.getroot()
    
  def traveBitmap(self, img):
    pass
  
  def splitPathAtMarkers(self):
    # Recherche de la balise path
    for path_elem_index, path_elem in enumerate(self.root.iter('path')):
        path_data = path_elem.get('d')
        if path_data:
            # Découper le chemin à chaque marqueur 'm' ou 'M'
            sub_paths = path_data.split('m') + path_data.split('M')

            # Créer des chemins indépendants avec un ID basé sur la position dans le fichier
            for i, sub_path in enumerate(sub_paths[1:]):  # Ignorer le premier élément vide
                new_path_elem = ET.Element('path')
                new_path_elem.set('d', 'M' + sub_path.strip())  # Ajouter 'M' au début de chaque sous-chemin
                new_path_elem.set('id', f'path_{path_elem_index}_{i}')
                self.root.insert(self.root.index(path_elem) + i + 1, new_path_elem)  # Insérer le nouvel élément après l'élément d'origine
            # Supprimer l'élément d'origine
            self.root.remove(path_elem)
    # Enregistrer le SVG modifié dans un nouveau fichier
    output_file_path = self.path.replace('.svg', '_modified.svg')
    self.tree.write(output_file_path)
    
  def getSvgDimensions(self):
    '''
    renvoie les dimensions du fichier svg
    '''
    # Recherche de la balise svg
    svg_elem = self.root.find('.//{http://www.w3.org/2000/svg}svg')  # Utilisation de l'espace de noms SVG
    
    if svg_elem is not None:
        width = svg_elem.get('width')
        height = svg_elem.get('height')
        return width, height
    return None, None
  
  def loopOverTag(self, tag, condition):
    return (path for path in self.root.iter(tag))
  
  def getPathStartPosition(self, target_path_id):
    '''
    renvoie la position du premier point du path dans le fichier
    '''
    #use loopOverTag generator
    # for self.loopOverTag('path'):
    # Recherche de la balise path
    for path_elem in self.root.iter('path'):
        path_id = path_elem.get('id')
        if path_id == target_path_id:
            path_data = path_elem.get('d')
            if path_data:
                # Extraire les coordonnées du premier point du chemin
                first_point = path_data.split(' ', 1)[1].split(' ', 1)[0]
                return first_point

    return f"Le chemin avec l'ID {target_path_id} n'a pas été trouvé dans le fichier SVG."
  
  def extractPathsByPosition(self, parts: dict):
    '''
    extraits les paths en fonction de la position du premier point dans le fichier et les enregistre dans des fichiers svg differents
    '''
    
    for n in len(parts):
      parts[n] = ET.Element('svg')

    # Recherche de la balise path
    for path_elem in self.root.iter('path'):
        path_id = path_elem.get('id')
        if path_id:
            # Récupérer la position du chemin (gauche, milieu, droite)
            path_position = self.getPathStartPosition(path_id)
            #int(path_id.split('_')[-1])
            width, height = self.getSvgDimensions()
            
            # Copier le chemin dans le fichier approprié
            length = len(parts.keys())
            for i in range(length):
              if path_position < (i*width // length):
                parts[n].append(path_elem)
                 
    # Enregistrer les chemins dans trois fichiers différents
    for n in parts:
      #pourquoi pas utiliser parts[ng] direct ?
      parts_tree[n] = ET.ElementTree(parts[n])
      parts_tree[n].write(self.path.replace('.svg', f'_{n}.svg'))
  
  def removePathByStartPosition(self, target_start_position):

    # Recherche de la balise path
    for path_elem in self.root.iter('path'):
        path_data = path_elem.get('d')
        if path_data:
            # Extraire les coordonnées du premier point du chemin
            first_point = path_data.split(' ', 1)[1].split(' ', 1)[0]

            # Supprimer le chemin si les coordonnées correspondent à la position cible
            if first_point == target_start_position:
                self.root.remove(path_elem)
                
  def resizeSvg(self, width, height):
    # Charger le fichier SVG
    with open(self.path, 'r') as inputf:
        svg_data = inputf.read()
    # Redimensionner le SVG avec le même ratio
    svg_data_resized = cairosvg.transform.resize(svg_data, width=width, height=height)
    # Enregistrer le résultat dans un nouveau fichier
    with open(self.path.replace('.svg', '_resized.svg'), 'w') as outputf:
        outputf.write(svg_data_resized)
  
# Exemple d'utilisation
if __name__ == "__main__":
  parts = {'skull': None, 'body': None, 'hip':None, 'tail':None}
  svg_file_path = 'exemple.svg'
  
  im2svg = ImageToSvg(svg_file_path)
  im2svg.splitPathAtMarkers()
  im2svg.extractPathsByPosition(parts)