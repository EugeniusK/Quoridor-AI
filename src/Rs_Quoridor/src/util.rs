pub mod util {
    use crate::rand::Rng;
    use std::time::Instant;

    pub fn min_idx(list: &[usize]) -> usize {
        let mut smallest = &list[0];
        let mut smallest_idx = 0;
        let mut idx = 0;
        for item in list {
            if item < smallest {
                smallest = item;
                smallest_idx = idx;
            }
            idx += 1;
        }

        smallest_idx
    }
    pub fn find_idx(list: &[i16], val: i16) -> usize {
        for idx in 0..list.len() {
            if list[idx] == val {
                return idx;
            }
        }
        255
    }
    pub fn find_null(list: &[usize]) -> usize {
        for idx in 0..list.len() {
            if list[idx] == 255 {
                return idx;
            }
        }
        return 255;
    }

    pub fn find_nulli16(list: &[i16]) -> usize {
        for idx in 0..list.len() {
            if list[idx] == 255 {
                return idx;
            }
        }
        return 255;
    }

    pub fn min_idx_vec(list: &[usize; 81]) -> usize {
        list.iter()
            .position(|&x| x == *list.iter().min().unwrap())
            .unwrap()
    }

    pub fn min_idx_fix(list: &[usize; 81]) -> usize {
        let mut largest = &list[0];
        let mut largest_idx = 0;
        let mut idx = 0;
        for item in list {
            if item > largest {
                largest = item;
                largest_idx = idx;
            }
            idx += 1;
        }

        largest_idx
    }

    pub fn min_idx_vec_fix(list: &[usize]) -> usize {
        list.iter()
            .position(|&x| x == *list.iter().min().unwrap())
            .unwrap()
    }

    pub fn compare_min_idx(n: i32) {
        let mut rng = rand::thread_rng();

        let mut time_arr: f64 = 0.0;
        let mut time_vec: f64 = 0.0;
        let mut time_arr_fix: f64 = 0.0;
        let mut time_vec_fix: f64 = 0.0;
        let mut start: Instant;
        let mut arr: [usize; 81] = [0; 81];
        for _ in 0..n {
            let vec_random: Vec<usize> = (0..81).map(|_| rng.gen_range(0..5000)).collect();
            for x in 0..81 {
                arr[x] = vec_random[x];
            }
            for _ in 0..10 {
                start = Instant::now();
                min_idx(&arr);
                time_arr += start.elapsed().as_secs_f64();
                start = Instant::now();
                min_idx_vec(&arr);
                time_vec += start.elapsed().as_secs_f64();
                start = Instant::now();
                min_idx_fix(&arr);
                time_arr_fix += start.elapsed().as_secs_f64();
                start = Instant::now();
                min_idx_vec_fix(&arr);
                time_vec_fix += start.elapsed().as_secs_f64();
            }
        }
        println!("Array approach {} Vector approach {}", time_arr, time_vec);
        println!(
            "Array fixed approach {} Vector fixed approach {}",
            time_arr_fix, time_vec_fix
        );
    }
}
