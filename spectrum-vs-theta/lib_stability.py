"""
Reading stability information.

Defines a function extracted from Reader for the Fickett's model, which
reads files with stability information.

"""
import os


def get_stability_info(results_dir):
    """Read file with stability info for time series of detonation velocity.

    Returns
    -------
    eigvals : list
        List with eigenvalues. Each element is a dictionary
        with keys {'growth_rate', 'frequency'}.

    Raises
    ------
    ValueError
        If the file with stability information cannot be read.

    """
    eigvals = []

    fit_file = os.path.join(results_dir, 'stability.txt')

    if not os.path.isfile(fit_file):
        raise ValueError("Cannot find file 'stability.txt'.")

    with open(fit_file, 'r') as f:
        for line in f:
            # Skip file header.
            if line.startswith('#'):
                continue
            # Stop when meeting the sentinel of the eigenvalues list.
            if line.startswith('---'):
                break
            chunks = line.split()
            gr = float(chunks[0])
            fr = float(chunks[1])

            if len(eigvals):
                prev_eig = eigvals[-1]

                if type(prev_eig) is dict:
                    if fr == eigvals[-1]['frequency']:
                        eig_1 = eigvals.pop()
                        eig_2 = {'growth_rate': gr, 'frequency': fr}
                        eigs = [eig_1, eig_2]
                        eigvals.append(eigs)
                    else:
                        eig = {'growth_rate': gr, 'frequency': fr}
                        eigvals.append(eig)
                elif type(prev_eig) is list:
                    if fr == prev_eig[-1]['frequency']:
                        eigs = eigvals.pop()
                        eig_2 = {'growth_rate': gr, 'frequency': fr}
                        eigs.append(eig_2)
                        eigvals.append(eigs)
                    else:
                        eig = {'growth_rate': gr, 'frequency': fr}
                        eigvals.append(eig)
                else:
                    raise Exception('Cannot parse stability.txt')
            else:
                # Should be used only for the first line.
                eig = {'growth_rate': gr, 'frequency': fr}
                eigvals.append(eig)

    return eigvals
