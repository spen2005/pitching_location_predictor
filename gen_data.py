import numpy as np
import pandas as pd

def rotation_matrix(theta,phi):
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)

    cos_phi = np.cos(phi)
    sin_phi = np.sin(phi)
    
    matrix1 = np.array([[cos_theta, -sin_theta, 0],
                        [sin_theta, cos_theta, 0],
                        [0, 0, 1]])
    
    matrix2 = np.array([[cos_phi, 0, -sin_phi],
                        [0, 1, 0],
                        [sin_phi, 0, cos_phi]])

    return matrix2.dot(matrix1)

def camera(vector):
    x = vector[0]
    y = vector[1]
    z = vector[2]
    theta = np.arctan2(y,x)
    phi = np.pi-np.arctan2(np.sqrt(x**2 + y**2),z)
    return rotation_matrix(-theta,-phi)

def position_after_transformation(cam_pos,cam_view,point):
    point = point - cam_pos
    matrix = camera(cam_view)
    return matrix.dot(point)

def generate_data(n):
    # input data (vec1,vec2,...,vec8,timestamp,x',y',x,y,z)
    # 8 fixed points as information source
    dataset = []
    for i in range(n):
        # camera position (x,y,z)=(6~10,1,0~3)
        # camera view (x/sqrt(x^2+y^2+z^2),y/sqrt(x^2+y^2+z^2),z/sqrt(x^2+y^2+z^2)
        x = np.random.uniform(6,10)
        y = 1
        z = np.random.uniform(0,3)
        cam_pos = np.array([x,y,z])
        cam_view = np.array([x/np.sqrt(x**2+y**2+z**2),y/np.sqrt(x**2+y**2+z**2),z/np.sqrt(x**2+y**2+z**2)])
        # fixed points
        vec1 = np.array([0.91,1.585,0])
        vec2 = np.array([0.91,0.365,0])
        vec3 = np.array([-0.91,1.585,0])
        vec4 = np.array([-0.91,0.365,0])
        vec5 = np.array([0.91,-1.585,0])
        vec6 = np.array([0.91,-0.365,0])
        vec7 = np.array([-0.91,-1.585,0])
        vec8 = np.array([-0.91,-0.365,0])
        # transforamtion
        vec = position_after_transformation(cam_pos,cam_view,vec1)
        vec1_prime = np.array([vec[0]/vec[2],vec[1]/vec[2]])
        # *= x^2+y^2+z^2
        vec1_prime = vec1_prime*(x**2+y**2+z**2)
        vec = position_after_transformation(cam_pos,cam_view,vec2)
        vec2_prime = np.array([vec[0]/vec[2],vec[1]/vec[2]])
        vec2_prime = vec2_prime*(x**2+y**2+z**2)
        vec = position_after_transformation(cam_pos,cam_view,vec3)
        vec3_prime = np.array([vec[0]/vec[2],vec[1]/vec[2]])
        vec3_prime = vec3_prime*(x**2+y**2+z**2)
        vec = position_after_transformation(cam_pos,cam_view,vec4)
        vec4_prime = np.array([vec[0]/vec[2],vec[1]/vec[2]])
        vec4_prime = vec4_prime*(x**2+y**2+z**2)
        vec = position_after_transformation(cam_pos,cam_view,vec5)
        vec5_prime = np.array([vec[0]/vec[2],vec[1]/vec[2]])
        vec5_prime = vec5_prime*(x**2+y**2+z**2)
        vec = position_after_transformation(cam_pos,cam_view,vec6)
        vec6_prime = np.array([vec[0]/vec[2],vec[1]/vec[2]])
        vec6_prime = vec6_prime*(x**2+y**2+z**2)
        vec = position_after_transformation(cam_pos,cam_view,vec7)
        vec7_prime = np.array([vec[0]/vec[2],vec[1]/vec[2]])
        vec7_prime = vec7_prime*(x**2+y**2+z**2)
        vec = position_after_transformation(cam_pos,cam_view,vec8)
        vec8_prime = np.array([vec[0]/vec[2],vec[1]/vec[2]])
        vec8_prime = vec8_prime*(x**2+y**2+z**2)
        # start point = (17.44~18.44,-2~2,1.6~2.0) randomly sample
        # end point = (0,-2~2,-2~2) randomly sample
        x = np.random.uniform(17.44,18.44)
        y = np.random.uniform(-2,2)
        z = np.random.uniform(1.6,2.0)
        start_point = np.array([x,y,z])
        x = 0
        y = np.random.uniform(-2,2)
        z = np.random.uniform(-2,2)
        end_point = np.array([x,y,z])
        # segment (start,end) cut into 10 pieces 
        for t in range (0,10):
            timestamp = t
            x = start_point[0]+t*(end_point[0]-start_point[0])/10
            y = start_point[1]+t*(end_point[1]-start_point[1])/10
            z = start_point[2]+t*(end_point[2]-start_point[2])/10
            point = np.array([x,y,z])
            point_prime = position_after_transformation(cam_pos,cam_view,point)
            #add to the dataset
            data = []
            data.append(vec1_prime[0])
            data.append(vec1_prime[1])
            data.append(vec2_prime[0])
            data.append(vec2_prime[1])
            data.append(vec3_prime[0])
            data.append(vec3_prime[1])
            data.append(vec4_prime[0])
            data.append(vec4_prime[1])
            data.append(vec5_prime[0])
            data.append(vec5_prime[1])
            data.append(vec6_prime[0])
            data.append(vec6_prime[1])
            data.append(vec7_prime[0])
            data.append(vec7_prime[1])
            data.append(vec8_prime[0])
            data.append(vec8_prime[1])
            data.append(timestamp)
            data.append(point_prime[0])
            data.append(point_prime[1])
            data.append(point[0])
            data.append(point[1])
            data.append(point[2])
            dataset.append(data)
    #randomly sort the dataset then return
    np.random.shuffle(dataset)
    return dataset

# generate training data
train_data = generate_data(1000)
df = pd.DataFrame(train_data)
df.to_csv('train_data.csv',index=False)
print('train data generated')
# generate test data
test_data = generate_data(100)
df = pd.DataFrame(test_data)
df.to_csv('test_data.csv',index=False)
print('test data generated')

    


        