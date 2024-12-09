package utils

import (
	"fmt"
	"strconv"
	"strings"
	"time"

	"golang.org/x/exp/constraints"
)

func Must[T any](t T, err error) T {
	if err != nil {
		panic(err)
	}
	return t
}

func ParseInt(s string) int64 {
	return Must(strconv.ParseInt(s, 10, 64))
}

func ParseInts(s string, delim string) []int64 {
	ints := []int64{}
	for _, part := range strings.Split(s, delim) {
		ints = append(ints, ParseInt(part))
	}
	return ints
}

func Zip[T any](left, right []T) <-chan [2]T {
	out := make(chan [2]T)
	go func() {
		for i := range left {
			out <- [2]T{left[i], right[i]}
		}
		close(out)
	}()
	return out
}

func Pairwise[T any](list []T) <-chan [2]T {
	out := make(chan [2]T)
	go func() {
		for i := 1; i < len(list); i++ {
			out <- [2]T{list[i-1], list[i]}
		}
		close(out)
	}()
	return out
}

func Abs[T constraints.Integer](a T) T {
	if a < 0 {
		return -a
	}
	return a
}

func Counter[T comparable](list []T) map[T]int64 {
	counter := make(map[T]int64)
	for _, item := range list {
		counter[item]++
	}
	return counter
}

func Permutation2[T any](list []T) <-chan [2]T {
	out := make(chan [2]T)
	go func() {
		for i := range list {
			for j := range list {
				if i != j {
					out <- [2]T{list[i], list[j]}
				}
			}
		}
		close(out)
	}()
	return out
}

func MeasureRuntime[R any](f func() R) func() R {
	return func() R {
		start := time.Now()
		res := f()
		elapsed := time.Since(start).Microseconds()
		fmt.Printf("Execution time: %d us\n", elapsed)
		return res
	}
}
