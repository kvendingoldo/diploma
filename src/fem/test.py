from fe.triangle import Triangle
from geometry.point import Point


tri = Triangle(Point(1, 2), Point(3, 4), Point(5, 6))
print(tri)



def main():
    lake_superior = read_poly("./tmp.poly")
    triangles = triangulate(lake_superior, 'pq20a.01D')

    print(generate_fe_list(triangles))
    show_mesh(triangles)
