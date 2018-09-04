import dijkstra
import numpy as np

TEST_TYPES = (
  np.float32, np.float64,
  np.uint64, np.uint32, np.uint16, np.uint8,
  np.int64, np.int32, np.int16, np.int8,
  np.bool
)

def test_dijkstra2d_10x10():
  for dtype in TEST_TYPES:
    values = np.ones((10,10,1), dtype=dtype)
    
    path = dijkstra.dijkstra(values, (0,0,0), (3,0,0))

    assert len(path) == 4
    assert np.all(path == np.array([
      [0,0,0],
      [1,1,0],
      [2,1,0],
      [3,0,0],
    ]))

    path = dijkstra.dijkstra(values, (0,0,0), (5,5,0))

    assert len(path) == 6
    assert np.all(path == np.array([
      [0,0,0],
      [1,1,0],
      [2,2,0],
      [3,3,0],
      [4,4,0],
      [5,5,0],
    ]))

    path = dijkstra.dijkstra(values, (0,0,0), (9,9,0))
    
    assert len(path) == 10
    assert np.all(path == np.array([
      [0,0,0],
      [1,1,0],
      [2,2,0],
      [3,3,0],
      [4,4,0],
      [5,5,0],
      [6,6,0],
      [7,7,0],
      [8,8,0],
      [9,9,0]
    ]))

def test_dijkstra2d_10x10_off_origin():
  for dtype in TEST_TYPES:
    values = np.ones((10,10,1), dtype=dtype)
    
    path = dijkstra.dijkstra(values, (2,0,0), (3,0,0))

    assert len(path) == 2
    assert np.all(path == np.array([
      [2,0,0],
      [3,0,0],
    ]))

    path = dijkstra.dijkstra(values, (2,1,0), (3,0,0))

    assert len(path) == 2
    assert np.all(path == np.array([
      [2,1,0],
      [3,0,0],
    ]))

    path = dijkstra.dijkstra(values, (9,9,0), (5,5,0))

    assert len(path) == 5
    assert np.all(path == np.array([
      [9,9,0],
      [8,8,0],
      [7,7,0],
      [6,6,0],
      [5,5,0],
    ]))

def test_dijkstra3d_3x3x3():
  for dtype in TEST_TYPES:
    values = np.ones((3,3,3), dtype=dtype)

    path = dijkstra.dijkstra(values, (0,0,0), (2,2,2))
    assert np.all(path == np.array([
      [0,0,0],
      [1,1,1],
      [2,2,2]
    ]))

    path = dijkstra.dijkstra(values, (2,2,2), (0,0,0))
    assert np.all(path == np.array([
      [2,2,2],
      [1,1,1],
      [0,0,0]
    ]))

def test_dijkstra_2d_loop():
  x = 20000
  values = np.array([
    [x, x, x, x, x, x, 0, x, x, x],
    [x, x, x, x, x, x, 0, x, x, x],
    [x, x, 1, x, 0, 0, 0, x, x, x],
    [x, x, 2, x, 0, x, 0, x, x, x],
    [x, 0, x, 3, x, x, 0, x, x, x],
    [x, 0, x, 4, 0, 0, 0, x, x, x],
    [x, 0, x, 5, x, x, x, x, x, x],
    [x, 0, x, 6, x, x, x, x, x, x],
    [x, 0, x, 7, x, x, x, x, x, x],
    [x, x, x, 1, 8, 9,10, x, x, x],
    [x, x, x, 4, x, x,11,12, x, x],
    [x, x, x, x, x, x, x, x,13,14],
  ])

  path = dijkstra.dijkstra(np.asfortranarray(values), (2,2), (11, 9))
  correct_path = np.array([
    [2, 2],
    [3, 2],
    [4, 3],
    [5, 4],
    [6, 3],
    [7, 3],
    [8, 3],
    [9, 4],
    [9, 5],
    [9, 6],
    [10, 7],
    [11, 8],
    [11, 9]
  ])

  assert np.all(path == correct_path)


def test_distance_field_2d():
  for dtype in TEST_TYPES:
    values = np.ones((5,5), dtype=dtype)
    
    field = dijkstra.distance_field(values, (0,0))

    assert np.all(field == np.array([
      [
        [0, 1, 2, 3, 4],
        [1, 1, 2, 3, 4],
        [2, 2, 2, 3, 4],
        [3, 3, 3, 3, 4],
        [4, 4, 4, 4, 4],
      ]
    ]))

    field = dijkstra.distance_field(values, (4,4))

    assert np.all(field == np.array([
      [
        [4, 4, 4, 4, 4],
        [4, 3, 3, 3, 3],
        [4, 3, 2, 2, 2],
        [4, 3, 2, 1, 1],
        [4, 3, 2, 1, 0],
      ]
    ]))

    field = dijkstra.distance_field(values, (2,2))

    assert np.all(field == np.array([
      [
        [2, 2, 2, 2, 2],
        [2, 1, 1, 1, 2],
        [2, 1, 0, 1, 2],
        [2, 1, 1, 1, 2],
        [2, 2, 2, 2, 2],
      ]
    ]))


    field = dijkstra.distance_field(values * 2, (2,2))

    assert np.all(field == np.array([
      [
        [4, 4, 4, 4, 4],
        [4, 2, 2, 2, 4],
        [4, 2, 0, 2, 4],
        [4, 2, 2, 2, 4],
        [4, 4, 4, 4, 4],
      ]
    ]))

def test_distance_field_2d_asymmetric():
  for dtype in TEST_TYPES:
    values = np.ones((5, 10), dtype=dtype)

    answer = np.array([
      [1, 0, 1, 2, 3, 4, 5, 6, 7, 8],
      [1, 1, 1, 2, 3, 4, 5, 6, 7, 8],
      [2, 2, 2, 2, 3, 4, 5, 6, 7, 8],
      [3, 3, 3, 3, 3, 4, 5, 6, 7, 8],
      [4, 4, 4, 4, 4, 4, 5, 6, 7, 8],
    ], dtype=np.float32)

    field = dijkstra.distance_field(values, (0,1))
    assert np.all(field == answer)


