/* Buggy ???

  for (int i = 0; i <= length_string1; i++)
    for (int j = 0; j <= length_string2; j++)
      distance_matrix[i][j] = -1;

  int distance(int i, int j) {
    if (distance_matrix[i][j] >= 0)
      return distance_matrix[i][j];

    int x;
    if (i == length_string1)
      x = length_string2 - j;
    else if (j == length_string2)
      x = length_string1 - i;
    else if (string1[i] == string2[j])
      x = distance(i + 1, j + 1);
    else {
      x = distance(i + 1, j + 1);

      int y;
      if ((y = distance(i, j + 1)) < x)
        x = y;
      if ((y = distance(i + 1, j)) < x)
        x = y;
      x++;
    }

    return distance_matrix[i][j] = x;
  }

  return distance(0, 0);
*/
